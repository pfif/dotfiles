from collections import OrderedDict

import scrapy


class VocabularyCom(scrapy.Spider):
    name = "Vocabulary.com mastered vocabulary exporter"

    def start_requests(self):
        return [
            scrapy.http.FormRequest(
                "https://www.vocabulary.com/login/",
                formdata={
                    "username": "florent.pastor@gmail.com",
                    "password": "(enterpasswordhere)"
                },
                headers={
                    "Referer": "https://www.vocabulary.com/login/"
                },
                callback=self.logged_in
            )
        ]

    def logged_in(self, response):
        return response.follow("https://www.vocabulary.com/account/progress/words/mastered", callback=self.vocabulary_page)

    def vocabulary_page(self, response):
        for words in response.css(".words > li > a"):
            yield OrderedDict([
                ("Word", words.css("span.word::text").extract_first()),
                ("Definition", words.css("dfn::text").extract_first()),
                ("Example", ""),
            ])
