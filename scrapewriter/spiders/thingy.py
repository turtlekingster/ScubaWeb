# -*- coding: utf-8 -*-
import scrapy
from scrapewriter.items import FurAffinityViewPage

class ThingySpider(scrapy.Spider):
    name = 'thingy'
    def start_requests(self):
        init_url = 'https://furaffinity.net/browse/'
	start_urls = [init_url]
	page_count = 991
	for i in range(2, page_count):
		start_urls.append(init_url + str(i) + '/')
	for url in start_urls:
		yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
	items =[]    
	#selects view page links
	for href in response.selector.xpath('//a[contains(@href, "view")]/@href').extract():
		item = FurAffinityViewPage(href = href, key = href.split("/")[2])
		items.append(item)

	return items

