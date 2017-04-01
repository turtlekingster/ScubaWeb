"""
Item Exporters are used to export/serialize items into sqlite3 database.
"""
import sqlite3

class SqliteHandler:
    
    def __init__(self, conn):
        self.conn = conn
    def __del__(self):
	self.conn.close() 
