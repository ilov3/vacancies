# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Vacancy(scrapy.Item):
    title = scrapy.Field()
    salary = scrapy.Field()
    currency = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
