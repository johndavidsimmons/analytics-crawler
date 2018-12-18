# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScriptCheckItem(scrapy.Item):
    url = scrapy.Field()
    channel = scrapy.Field()
    script = scrapy.Field()
    script_exists = scrapy.Field()
    last_checked = scrapy.Field(serializer=str)
