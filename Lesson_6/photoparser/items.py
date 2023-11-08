# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import TakeFirst, MapCompose, Compose



def process_category(value):
    value = value.replace('\u00f3', ' ')
    return value

def process_photo(value:str):
    
    value = value.split()

    return value



class PhotoparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor = TakeFirst())

    photos = scrapy.Field(input_processor=MapCompose(process_photo))
    # photos = scrapy.Field(output_processor = TakeFirst())

    url = scrapy.Field(output_processor=TakeFirst())
    
    category = scrapy.Field(output_processor=MapCompose(process_category))

    _id = scrapy.Field()
    pass
