# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScriptCheckItem(scrapy.Item):
    common_name = scrapy.Field()
    prop = scrapy.Field()
    url = scrapy.Field()
    mparticle_exists = scrapy.Field()
    dtm_exists = scrapy.Field()
    last_checked = scrapy.Field(serializer=str)
