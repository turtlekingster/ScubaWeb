# -*- coding: utf-8 -*-
import scrapy
from scrapewriter.items import FurAffinityViewPage
from scrapewriter.items import StoryItem
from scrapewriter.converters import FileConverter
import sqlite3
import urllib2

class FurAffinityStage2Spider(scrapy.Spider):
    name = 'stage2'
    def start_requests(self):
	con = sqlite3.connect("sqllite.db")
	con.text_factory = str
	cur = con.cursor()
        init_url = 'https://furaffinity.net'
	cur.execute("select * from FurAffinityViewPage")
	maxrange = 4 #cur.rowcount
	start_urls = []
	for i in range(0 , maxrange):
		start_urls.append(init_url + cur.fetchone()[0])
	for url in start_urls:
		yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):    
	#selects view page links
	url = "http:" + str(response.selector.xpath('//a[contains(@href, "d.facdn.net")]/@href').extract_first())
	conv = FileConverter(url)
	text = conv.txt
	title = response.selector.xpath('//b/text()').extract_first()
	author = response.selector.xpath('//a[contains(@href, "/user/")]/text()').extract_first()
	tags = response.selector.xpath('//a[contains(@href, "@keywords")]/text()').extract()
	pub_date = response.selector.xpath('//span/@title').extract()[0] #convert to unix-time
	sub_id = response.url.split("/")[4]
	table_key = "FurAffintyViewPage"
	item = StoryItem(text=text, author=author, title=title, tags=tags, pub_date=pub_date, sub_id=sub_id, table_key=table_key)

	return item

