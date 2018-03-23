from collections import OrderedDict
from csv import DictReader
from urllib.parse import unquote
import re

from scrapy.http import Request
import scrapy


class JishoOrgWordSpider(scrapy.Spider):
    name = "JishoOrgSpider"

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

        return OrderedDict([
            ("Kanji", word_in_kanjis),
            ("English", definition),
            ("Example", ""),
            ("Furigana", word_in_hiragana),
        ])
