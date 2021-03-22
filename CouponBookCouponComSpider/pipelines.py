# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb
import mysql.connector

from CouponBookCouponComSpider.dbconfig import get_db_conn


class MysqlPipeline(object):
    def __init__(self):
        self.conn = get_db_conn()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql, params = item.get_insert_sql()

        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()
        return item

    def close_spider(self):
        self.conn.close()
