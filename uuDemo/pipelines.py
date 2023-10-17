# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UudemoPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = '饰品TOP'
        self.ws.append(('名字', '排名', '价格'))

    def close_spider(self, spider):
        self.wb.save('饰品.xlsx')

    def process_item(self, item, spider):
        name = item.get('name', '')
        rank = item.get('rank', '')
        price = item.get('price', '')
        self.ws.append((name, rank, price))
        return item
