# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UudemoItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    game_id = scrapy.Field()
    profit_margin = scrapy.Field()
    price = scrapy.Field()
    purchase_price = scrapy.Field()
    on_sale_count = scrapy.Field()
    exterior = scrapy.Field()
    icon_urlLarge = scrapy.Field()
    ob_url = scrapy.Field()
    uu_url = scrapy.Field()

