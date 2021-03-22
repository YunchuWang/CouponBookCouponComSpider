import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CouponBookCouponComSpider.items import Coupon, CouponComCouponLoader, MerchantLoader, Merchant
from CouponBookCouponComSpider.utils.common import get_md5


class CouponcomSpider(CrawlSpider):
    name = 'couponcom'
    allowed_domains = ['www.coupons.com']
    start_urls = ['https://www.coupons.com']
    rules = (
        # Rule(LinkExtractor(allow=r'/coupons/$'), callback='parse_printable_coupons', follow=False),
        Rule(LinkExtractor(allow=r'/store-loyalty-card-coupons/$'), follow=True),
        Rule(LinkExtractor(allow=r"/store-loyalty-card-coupons/([a-z]+-)+coupons/$"),
             callback='parse_merchant_coupon_page', follow=False)
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse_printable_coupons(self, response):
        # coupons = response.css('div.pod')
        # for coupon in coupons:
        #     if coupon.css('span.external-pod-link').get():
        #         continue
        #     item_loader = CouponComCouponLoader(item=Coupon(), selector=coupon)
        #     item_loader.add_css('id', '.coupon::attr(data-podid)', self.process_id)
        #     item_loader.add_css('title', '.summary::text')
        #     item_loader.add_css('description', '.details::text')
        #     item_loader.add_css('imageUrl', '.pod-image::attr(src)', self.process_link)
        #     parsedCoupon = item_loader.load_item()
        #     yield parsedCoupon
        pass

    def parse_digital_coupons(self, merchant_id, response):
        coupons = response.css('div.pod')
        for coupon in coupons:
            coupon_loader = CouponComCouponLoader(item=Coupon(), selector=coupon)
            coupon_loader.add_css('id', '.pod::attr(data-podid)', self.process_coupon_id)
            coupon_loader.add_css('title', '.pod_summary::attr(data-summary)')
            coupon_loader.add_css('description', '.pod_description::text')
            coupon_loader.add_value('merchantId', merchant_id)
            coupon_loader.add_css('imageUrl', 'div.media-object img::attr(src)', self.process_link)
            yield coupon_loader.load_item()

    def parse_merchant_coupon_page(self, response):
        # parse merchant
        merchant = self.parse_merchant(response)
        if merchant is None:
            return
        yield merchant

        # parse coupons
        for parsed_coupon in self.parse_digital_coupons(merchant['id'], response):
            yield parsed_coupon

    def parse_merchant(self, response):
        title = response.css('div.store-title .title::text').get()
        name_pattern = re.compile('https://www.coupons.com/store-loyalty-card-coupons/(.*)-coupons/')
        names = name_pattern.findall(response.url)
        if len(names) == 0:
            return
        merchant_name = names[0]
        merchant_loader = MerchantLoader(item=Merchant(), response=response)
        merchant_loader.add_value('id', get_md5(response.url))
        merchant_loader.add_value('name', merchant_name)

        logo_url = response.css('div.store-logo img::attr(src)')
        if not logo_url:
            # get from card coupon page elements
            logo_url = response.css('div.mod-storeinfo .top-content .pull-left div img::attr(src)').get()
        merchant_loader.add_value('logoUrl', [logo_url], self.process_link)
        merchant_loader.add_value('siteUrl', response.url)

        return merchant_loader.load_item()

    def process_id(self, ids):
        if not ids:
            return
        return int(ids[0])

    def process_coupon_id(self, ids):
        if not ids:
            return
        return get_md5(ids[0])

    def process_link(self, links):
        if not links:
            return
        link = links[0]

        return link if link.startswith("http") else ("https:" + link)
