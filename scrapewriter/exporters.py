"""
Item Exporters are used to export/serialize items into sqlite3 database.
"""
from scrapewriter.items import FurAffinityViewPage
from scrapewriter.items import StoryItem
from scrapy.exporters import BaseItemExporter
import sqlite3

class SqliteStoryItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.conn = sqlite3.connect(":memory:")
        self.db_file = sqlite3.connect(file.name)
        self.db_file.text_factory = str
        self.conn.text_factory = str
        self.created_tables = []

    def export_item(self, item):
        item_class_name = item.__class__.__name__
	
        if item_class_name not in self.created_tables:
		cols = item.keys()
		cols.remove('sub_id')
                self._create_table(item_class_name, cols, 'sub_id')
                self.created_tables.append(item_class_name)

        field_list = item.keys()
        value_list = item.values()
        sql = 'insert or ignore into [%s] (%s) values (%s)' % (item_class_name, ', '.join(field_list), ', '.join(['?' for f in field_list]))
	print 'sql: %s' % sql
        self.conn.execute(sql, value_list)
        self.db_file.execute(sql, value_list)

    def _create_table(self, table_name, columns, key):
        sql = 'create table if not exists [%s]' % table_name
        column_define = ' (' 
	for col in columns :
		column_define += '[%s] text, ' % col
        column_define += '[%s] UNSIGNED BIG INT PRIMARY KEY)' % key
        sql += column_define

        print 'sql: %s' % sql
        self.conn.execute(sql)
        self.db_file.execute(sql)
        self.conn.commit()
        self.db_file.execute(sql)

    def __del__(self):
        self.db_file.commit()
        self.db_file.close()
        self.conn.close()



class SqlitePageItemExporter(BaseItemExporter):
    
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.conn = sqlite3.connect(":memory:")
	self.db_file = sqlite3.connect(file.name)
	self.db_file.text_factory = str
        self.conn.text_factory = str
    	self.created_tables = []
    
    def export_item(self, item):
        item_class_name = item.__class__.__name__
    	if item_class_name not in self.created_tables:
    		self._create_table(item_class_name, "Href", "Key")
    		self.created_tables.append(item_class_name)
		
    	field_list = ["Href","Key"]
	value_list = [item['href'], item['key']]
    	sql = 'insert or ignore into [%s] (%s) values (%s)' % (item_class_name, ', '.join(field_list), ', '.join(['?' for f in field_list]))
    	self.conn.execute(sql, value_list)
	self.db_file.execute(sql, value_list)
    	self.conn.commit()
    		 
    def _create_table(self, table_name, column, key):
		sql = 'create table if not exists [%s]' % table_name
		
		column_define = ' ([%s] text' % column
		column_define += ', [%s] UNSIGNED BIG INT PRIMARY KEY)' % key
		
		sql += column_define
		
		print 'sql: %s' % sql
		self.conn.execute(sql)
		self.db_file.execute(sql)
		self.conn.commit()
		self.db_file.execute(sql)
    	
    def __del__(self):
	self.db_file.commit()
	self.db_file.close()
    	self.conn.close()
