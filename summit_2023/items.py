# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZquadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_id = scrapy.Field()  # UUID Validation
    name = scrapy.Field()  # Strip spaces
    image_id = scrapy.Field()  # UUID Validation
    rating = scrapy.Field()  # Strip spaces
