# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class Coupon(scrapy.Item):
    id = scrapy.Field()
    merchantId = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    volume = scrapy.Field()
    description = scrapy.Field()
    expirationTime = scrapy.Field()
    imageUrl = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT IGNORE INTO coupon (id, title, merchantId, url, description, imageUrl) VALUES (%s,%s,%s,%s,%s,%s) 
        """

        params = list()

        params.append(self.get("id", ""))
        params.append(self.get("title", ""))
        params.append(self.get("merchantId", -1))
        params.append(self.get("url", ""))
        params.append(self.get("description", ""))
        params.append(self.get("imageUrl", ""))

        return insert_sql, params


class CouponComCouponLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class Merchant(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    logoUrl = scrapy.Field()
    siteUrl = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT IGNORE INTO merchant (id, name, logoUrl, siteUrl) VALUES (%s,%s,%s,%s);
                """

        params = list()
        params.append(self.get("id", ""))
        params.append(self.get("name", ""))
        params.append(self.get("logoUrl", ""))
        params.append(self.get("siteUrl", ""))

        return insert_sql, params


class MerchantLoader(ItemLoader):
    default_output_processor = TakeFirst()
