# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import time

import scrapy
from pip._internal.utils import logging
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import add_cookies


class UudemoSpiderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)


class UudemoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 检查 request.url 是否以特定前缀开头
        if request.url.startswith('https://www.csgoob.com/goods?name='):
            chrome_driver = spider.driver
            chrome_driver.get(request.url)

            time.sleep(7)
            #下载buff数据
            download_btn = chrome_driver.find_element(By.CSS_SELECTOR, 'body > div.w-full.min-h-full.bg-light.text-black-85.dark\:text-light.dark\:bg-dark > div.w-full.h-full.mt-16.pt-6 > div > div.w-full.lg\:w-2\/3.px-2 > div:nth-child(1) > div.flex.flex-col > div.dark\:shadow-none.card-shadow.relative.bg-white.dark\:bg-dark-light.rounded-2xl.mb-6.w-full.flex-1.relative.overflow-hidden > div.w-watermark-wrapper.w-full.h-full.relative.flex.flex-col > div.absolute.left-4.top-1.flex.space-x-2.items-center > span:nth-child(3) > svg')
            download_btn.click()
            time.sleep(0.5)
            # #下载uu有品求购数据
            # nav_btn = chrome_driver.find_element(By.CSS_SELECTOR, 'body > div.w-full.min-h-full.bg-light.text-black-85.dark\:text-light.dark\:bg-dark > div.w-full.h-full.mt-16.pt-6 > div > div.w-full.lg\:w-2\/3.px-2 > div.flex.flex-col > div.dark\:shadow-none.card-shadow.relative.bg-white.dark\:bg-dark-light.rounded-2xl.mb-6.w-full.flex-1.relative.overflow-hidden > div.w-watermark-wrapper.w-full.h-full.relative.flex.flex-col > div.absolute.right-4.top-0.z-10 > span:nth-child(2)')
            # nav_btn.click()
            # time.sleep(0.5)
            # uu_btn =  chrome_driver.find_element(By.CSS_SELECTOR, 'ul[data-menu-list="true"] li[data-menu-id*="-1"] span')
            #
            # uu_btn.click()
            # time.sleep(5)
            # download_btn = chrome_driver.find_element(By.CSS_SELECTOR,
            #                                           'body >  div.absolute.left-4.top-1.flex.space-x-2.items-center > span:nth-child(3) > svg')
            # #download_btn.click()

            return HtmlResponse(url=spider.driver.current_url, body=spider.driver.page_source, encoding='utf-8')

        elif request.url.startswith('https://www.youpin898.com/goodInfo?id='):
            # 如果 URL 以指定前缀开头，执行特殊处理
            spider.driver.get(request.url)
            add_cookies(spider.driver, 'uu.json')
            time.sleep(1)

            close_btn = spider.driver.find_element(By.CSS_SELECTOR, 'button.ant-modal-close')
            close_btn.click()
            time.sleep(3)

            try:
                wait = WebDriverWait(spider.driver, 10)
                get_btn = spider.driver.find_element(By.CSS_SELECTOR,
                                                     'div[role="tab"][aria-disabled="false"][aria-selected="true"].ant-tabs-tab-active.ant-tabs-tab')
                get_btn.click()
                time.sleep(3)
                self.logger.info("成功点击按钮！")  # 添加成功的日志记录
                # 执行特殊处理后，可以返回 Response 对象，Request 对象或 None
                # 例如：
                return HtmlResponse(url=spider.driver.current_url, body=spider.driver.page_source, encoding='utf-8')

            except NoSuchElementException:
                # 处理元素未找到的异常
                self.logger.error("元素未找到，无法执行点击操作")

            except Exception as e:
                # 处理其他可能的异常
                self.logger.error(f"发生异常: {str(e)}")

        return None

    def _wait_for_file(self, file_name, timeout=60):
        start_time = time.time()
        file_path = os.path.join(self.download_dir, file_name)
        while not os.path.exists(file_path):
            if time.time() - start_time > timeout:
                raise TimeoutError(f"File download timeout for {file_name}")
            time.sleep(1)

    def download_file(self, file_name, timeout=60):
        self._wait_for_file(file_name, timeout)
        file_path = os.path.join(self.download_dir, file_name)
        return file_path

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

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
        spider.logger.info("Spider opened: %s" % spider.name)
