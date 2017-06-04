# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AutocrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Main scrapy.fields 

    vehicle_ref_no = scrapy.Field()
    vehicle_make = scrapy.Field()
    vehicle_model = scrapy.Field()
    vehicle_year = scrapy.Field()
    vehicle_engine = scrapy.Field()
    vehicle_transmission = scrapy.Field()
    vehicle_fuel = scrapy.Field()
    vehicle_price_fob = scrapy.Field()
    vehicle_price_cif = scrapy.Field()
    vehicle_description = scrapy.Field()
    vehicle_title = scrapy.Field()
    vehicle_drive = scrapy.Field()
    vehicle_steering = scrapy.Field()
    vehicle_color = scrapy.Field()
    vehicle_doors = scrapy.Field()
    vehicle_seats = scrapy.Field()
    vehicle_body = scrapy.Field()
    vehicle_mileage = scrapy.Field()
    vehicle_accessories = scrapy.Field() 
    vehicle_thumbnails = scrapy.Field() 

    #tracking scrapy.fields 
    url = scrapy.Field()
    project = scrapy.Field()
    spider  = scrapy.Field()
    server  = scrapy.Field()
    crawled_date = scrapy.Field() 
    pass
