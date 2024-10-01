# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pymongo

class DebateCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    topic_name = scrapy.Field()
    motion = scrapy.Field()
    points_for = scrapy.Field()
    points_against = scrapy.Field()
    bibliography = scrapy.Field()
    post_type = scrapy.Field()
    post_date = scrapy.Field()
    describe = scrapy.Field()

    pass
