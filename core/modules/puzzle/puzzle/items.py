# -*- coding: UTF-8 -*-
# Creator：LeK
# Date：2022/11/14

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class PuzzleItemLoader(ItemLoader):  # 自定义itemloader,用于存储爬虫所抓取的字段内容
    default_output_processor = TakeFirst()


class CymyItem(scrapy.Item):  # 建立相应的字段
    mystery = scrapy.Field()  # 谜面
    tips = scrapy.Field()  # 提示
    answer = scrapy.Field()  # 谜底


class ZmmyItem(scrapy.Item):  # 建立相应的字段
    mystery = scrapy.Field()  # 谜面
    tips = scrapy.Field()  # 提示
    answer = scrapy.Field()  # 谜底


class DwmyItem(scrapy.Item):  # 建立相应的字段
    mystery = scrapy.Field()  # 谜面
    tips = scrapy.Field()  # 提示
    answer = scrapy.Field()  # 谜底

class DmmyItem(scrapy.Item):  # 建立相应的字段
    mystery = scrapy.Field()  # 谜面
    tips = scrapy.Field()  # 提示
    answer = scrapy.Field()  # 谜底