# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StoryItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    text = scrapy.Field()
    pub_date = scrapy.Field()
    sub_id = scrapy.Field()
    table_key = scrapy.Field()
    #pass

class FurAffinityViewPage(scrapy.Item):
    href = scrapy.Field()
    key = scrapy.Field()

