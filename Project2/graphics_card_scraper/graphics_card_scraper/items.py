# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GraphicsCardScraperItem(scrapy.Item):
    item_id = scrapy.Field()
    title = scrapy.Field()
    branding = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    price = scrapy.Field()
    shipping = scrapy.Field()
    image_url = scrapy.Field()
    max_resolution = scrapy.Field()
    displayport = scrapy.Field()
    hdmi = scrapy.Field()
    directx = scrapy.Field()
    model = scrapy.Field()
