from csv import DictReader, DictWriter
from urllib.parse import unquote
import re

from scrapy.exporters import BaseItemExporter
from scrapy.http import Request
import scrapy


class JishoOrgWordSpider(scrapy.Spider):
    name = "JishoOrgSpider"
    custom_settings = {
        "ITEM_PIPELINES": {
            "jisho_org_scrapper.MemriseJapaneseVocabularyExporterPipeline": 100
        }
    }

    def start_requests(self):
        with open(self.settings.get("VOCABULARY_FILE_LOCATION")) as vocabulary_file:
            vocabulary_csv_reader = DictReader(vocabulary_file, ["URL", "index_of_definition"])
            for row in vocabulary_csv_reader:
                yield Request(row["URL"], meta={"index_of_definition": int(row["index_of_definition"]) - 1})

    def parse(self, response):
        # Find definition
        definition = response.css(".meaning-meaning::text").extract()[response.meta["index_of_definition"]]

        # Find kanjis
        word_in_kanjis = unquote(response.request.url.split("/")[-1])

        # Find hiraganas
        furigana_span_elements = response.css(".concept_light-representation > .furigana > span").extract()  # One element per characters in the 'kanjis' string

        furigana_regex = "<span .*>(.*)</span>"  # Match only with elements that contains furiganas
        furigana_characters_regex_matches = [re.match(furigana_regex, element) for element in furigana_span_elements]

        if set(furigana_characters_regex_matches) is None:  # No furigana found
            word_in_hiragana = None
        else:
            furigana_and_kanji_mixed_characters = [
                match.group(1) if match else word_in_kanjis[i]
                for i, match in enumerate(furigana_characters_regex_matches)
            ]

            word_in_hiragana = "".join(furigana_and_kanji_mixed_characters)

        return {
            "definition": definition,
            "word_in_kanjis": word_in_kanjis,
            "word_in_hiragana": word_in_hiragana
        }


class MemriseJapaneseVocabularyExporterPipeline(object):
    def open_spider(self, spider):
        self.exporter = MemriseJapaneseVocabularyExporter()
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)

    def close_spider(self, spider):
        self.exporter.finish_exporting()


class MemriseJapaneseVocabularyExporter(BaseItemExporter):
    def start_exporting(self):
        self.kanji_file = open("memrise_japanese_vocabulary_kanjis.csv", "w")
        self.hiragana_file = open("memrise_japanese_vocabulary_hiragana.csv", "w")

        csv_fields = [
            "Kana",
            "English",
            "Common Japanese",
            "Kanji",
            "Part of Speech",
            "Gender"
        ]
        self.kanji_csvdictwriter = DictWriter(self.kanji_file, csv_fields)
        self.hiragana_csvdictwriter = DictWriter(self.hiragana_file, csv_fields)

    def export_item(self, item):
        self.kanji_csvdictwriter.writerow({
            "Kana": item["word_in_kanjis"],
            "English": item["definition"],
            "Common Japanese": "",
            "Kanji": item["word_in_hiragana"] if item["word_in_hiragana"] else "",
            "Part of Speech": "",
            "Gender": "",
        })

        if item["word_in_hiragana"]:
            self.hiragana_csvdictwriter.writerow({
                "Kana": item["word_in_hiragana"],
                "English": item["definition"],
                "Common Japanese": "",
                "Kanji": item["word_in_kanjis"],
                "Part of Speech": "",
                "Gender": "",
            })

    def finish_exporting(self):
        self.kanji_file.close()
        self.hiragana_file.close()
