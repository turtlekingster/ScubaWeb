# -*- coding: utf-8 -*-
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.furaffinity.net/browse/',
    ]

    def parse(self, response):
        for quote in response.xpath("figcaption"):
            yield {
                'text': quote.css("t-image").extract_first(),
            }

        #next_page_url = response.css("li.next > a::attr(href)").extract_first()
        #if next_page_url is not None:
        #    yield scrapy.Request(response.urljoin(next_page_url))

