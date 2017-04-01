import scrapy
from scrapy.crawler import CrawlerProcess

import scrapewriter
from scrapewriter.items import FurAffinityViewPage
from scrapewriter.items import StoryItem
from scrapewriter.converters import FileConverter
from scrapewriter.spiders import thingy
from scrapewriter.spiders import furaffinitystage2
from scrapewriter import settings
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())


process.crawl(thingy)
process.start()


