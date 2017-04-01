# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapewriterPipeline(object):
    def process_item(self, item, spider):
        return item


# pipelines.py
import logging

from scrapy import signals
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()

class Book(DeclarativeBase):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    author = Column('author', String)
    publisher = Column('publisher', String)
    url = Column('url', String)
    scrape_date = Column('scrape_date', DateTime)

    def __repr__(self):
        return "<Book({})>".format(self.url)


class SqlitePipeline(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')
        self.sessions = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def create_engine(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool)
        return engine

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()

    def process_item(self, item, spider):
        session = self.sessions[spider]
        book = Book(**item)
        link_exists = session.query(Book).filter_by(url=item['url']).first() is not None

        if link_exists:
            logger.info('Item {} is in db'.format(book))
            return item

        try:
            session.add(book)
            session.commit()
            logger.info('Item {} stored in db'.format(book))
        except:
            logger.info('Failed to add {} to db'.format(book))
            session.rollback()
            raise

        return item
