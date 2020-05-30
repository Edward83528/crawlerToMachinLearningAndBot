# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    ip = scrapy.Field()
    comments = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    updatetime = scrapy.Field()
    board = scrapy.Field()
    locale = scrapy.Field()

    