# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JDDataItem(Item):
    item_name = Field()
    item_code = Field()
    item_data = Field()
    item_unit = Field()
