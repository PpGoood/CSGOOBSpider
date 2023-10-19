import json
import os
import urllib
import random

import pandas as pd
import scrapy
from scrapy import Selector
from scrapy.http import HtmlResponse
from uuDemo.items import UudemoItem
import time
from pydispatch import dispatcher
from scrapy import signals
from utils import create_chrome_driver, add_cookies
from datetime import datetime, timedelta
class UuSpider(scrapy.Spider):
    name = "uu"
    allowed_domains = ["www.csgoob.com"]

    def __init__(self, *args, **kwargs):
        self.driver = create_chrome_driver()
        add_cookies(self.driver, 'uu.json')
        time.sleep(5)
        super(UuSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.close_driver, signals.spider_closed)

    def start_requests(self):
        time.sleep(1)
        file_path = r'G:\Desktop\python项目\uuDemo\merged.json'
        cur_count = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        #获取data长度 计数来显示进度
        for index, data_one in enumerate(data):
            cur_count = cur_count + 1
            # self.logger.debug(f"data_one content: {data_one}")
            csgoitem = self.init_csgoitem(data_one=data_one, index=index + 1)
            if self.check_file(csgoitem=csgoitem):
                yield scrapy.Request(url=csgoitem['ob_url'], callback=self.parse_csobdata, meta={'item': csgoitem})
                # yield scrapy.Request(url=csgoitem['uu_url'], callback=self.parse_csuudata, meta={'item': csgoitem})


    def check_file(self, csgoitem):
        folder_path = r'G:\Desktop\python项目\uuDemo\dataExcel'  # 修改为你的文件夹路径
        # 构建文件名，将特殊字符替换为下划线
        file_name1 = '【' + csgoitem['name'].replace(' | ', ' _ ') + '】悠悠有品近1个月-总览.xlsx'
        file_name2 = '【' + csgoitem['name'].replace(' | ', ' _ ') + '】Buff近1个月-总览.xlsx'
        # 拼接文件的完整路径
        file_path1 = os.path.join(folder_path, file_name1)
        file_path2 = os.path.join(folder_path, file_name2)

        file_path = None
        print("检查文件是否存在",csgoitem['name'],os.path.exists(file_path1) and os.path.exists(file_path2))
        # 检查文件是否存在
        # if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        #     return True
        # if os.path.exists(file_path1):
        #     isNeed1 = self.process_file(file_path1,csgoitem)
        # if os.path.exists(file_path2):
        #     isNeed2 = self.process_file(file_path2,csgoitem)
        # return isNeed1 or isNeed2
        startRule = "1"
        if startRule == "1":
            if not os.path.exists(file_path1):
                return True
            else:
                return self.process_file(file_path1, csgoitem)
        elif startRule == "2":
            if not os.path.exists(file_path2):
                return True
            else:
                return self.process_file(file_path2, csgoitem)






    def process_file(self,file_path, csgoitem):
        # 获取文件的最后修改时间
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

        # 获取当前时间
        current_time = datetime.now()

        # 计算时间差
        time_difference = current_time - file_modified_time
        hours_difference = time_difference.total_seconds() / 3600

        # 更改时间算法，从csgo_uu求购利润率此文件去获取该文件
        min_interval_time = 12

        file_profit = r'G:\Desktop\python项目\uuDemo\csgo_uu求购利润率.xlsx'
        # 读取Excel文件
        df = pd.read_excel(file_profit)

        # 获取第一行的利润率作为最大利润率
        max_profit_rate = df.iloc[0]['利润率']

        # 获取最后一行的利润率作为最小利润率
        min_profit_rate = 0

        item_profit_rate = df.loc[df['武器名'] == csgoitem['name'].replace(' | ', ' _ '), '利润率'].values[0]
        if item_profit_rate < 0:
            item_profit_rate = 0

        if item_profit_rate >= 0.1:
            max_interval_time = 12
        elif item_profit_rate >= 0.075:
            max_interval_time = 24
        elif item_profit_rate >= 0.05:
            max_interval_time = 36
        else:
            max_interval_time = 48

        # 利润值对时间间隔的逆向线性映射
        normalized_profit = 1 - (item_profit_rate + min_profit_rate) / (max_profit_rate + min_profit_rate)
        crawl_interval = min_interval_time + normalized_profit * (max_interval_time - min_interval_time)

        print("利润", item_profit_rate, "动态时间:", hours_difference,crawl_interval)
        # 如果时间差超过 crawl_interval 小时，删除文件并返回 True
        if hours_difference > crawl_interval:
            os.remove(file_path)
            return True

        return False
    def init_csgoitem(self, data_one, index):
        csgo_item = UudemoItem()
        csgo_item['id'] = index
        csgo_item['name'] = data_one['CommodityName']
        csgo_item['game_id'] = data_one['GameId']
        csgo_item['profit_margin'] = '0%'
        csgo_item['price'] = data_one['Price']
        csgo_item['purchase_price'] = '0'
        csgo_item['on_sale_count'] = data_one['OnSaleCount']
        csgo_item['exterior'] = data_one['Exterior']
        csgo_item['icon_urlLarge'] = data_one['IconUrlLarge']
        encoded_url = urllib.parse.quote(f"https://www.csgoob.com/goods?name={data_one['CommodityName']}", safe=':/?=&')
        csgo_item['ob_url'] = encoded_url
        csgo_item['uu_url'] = f"https://www.youpin898.com/goodInfo?id={data_one['Id']}"
        return csgo_item

    def parse_csobdata(self, response:HtmlResponse):
        time.sleep(10)
        item = response.meta['item']
        sel = Selector(response)
        price = sel.xpath('//span[@class="text-lg text-orange-400 mr-2 font-bold"]/text()').get()
        print("价格:", price)

        item['price'] = price

        yield item

    def parse_csuudata(self, response:HtmlResponse):
        item = response.meta['item']
        sel = Selector(response)
        item['purchase_price'] = sel.css(".text-orange-400").get()
        # 检查 purchase_price 是否为空
        self.logger.debug(f"data_one purchase_price: {item['purchase_price']}")

        if item['purchase_price'] < item['price']:
            result = "({0} - {1}) / {1} * 100".format(item['purchase_price'], item['price'])
            percentage_str = "{:.2f}%".format(round(float(result), 2))
            item['profit_margin'] = percentage_str

        yield item

    def close_driver(self):
        print("爬虫正在退出，执行关闭浏览器哦")
        time.sleep(2)
        self.driver.quit()