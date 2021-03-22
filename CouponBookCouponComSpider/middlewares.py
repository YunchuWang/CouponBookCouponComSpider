# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep
import re
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class CouponbookcouponcomspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CouponbookcouponcomspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # browser = webdriver.Chrome(
    #     executable_path="C:/Users/yunch/PycharmProjects/CouponBookCouponComSpider/selenium_drivers/chromedriver.exe",
    #     options=chrome_options)
    browser = webdriver.PhantomJS(executable_path="C:/Users/yunch/PycharmProjects/CouponBookCouponComSpider/selenium_drivers/phantomjs.exe")

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if request.url == 'https://www.coupons.com/coupons/':
            self.browser.get(request.url)
            sleep(5)
            load_more_button = self.browser.find_elements_by_xpath("//*[@id=\"main\"]/div[6]/div[3]/button")[0]
            load_more_button.click()
            sleep(5)
            body = self.browser.page_source
            return HtmlResponse(self.browser.current_url, body=body, encoding='utf-8', request=request)

        if re.match(r'https://www.coupons.com/store-loyalty-card-coupons/([a-z]+\-)+coupons/$', request.url):
            self.browser.get(request.url)
            sleep(5)
            self.scroll_down()
            body = self.browser.page_source
            return HtmlResponse(self.browser.current_url, body=body, encoding='utf-8', request=request)
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def scroll_down(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.browser.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
