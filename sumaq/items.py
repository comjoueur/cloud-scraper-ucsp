# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PostItem(Item):
    id = Field()
    post_body = Field()
    mention = Field()
