# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):

    url = scrapy.Field()
    book_name = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_of_reviews = scrapy.Field()
    avg_rating = scrapy.Field()
    book_category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()

