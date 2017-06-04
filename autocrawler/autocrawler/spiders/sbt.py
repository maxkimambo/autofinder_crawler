# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import logging 
log = logging.getLogger()
from autocrawler.items import AutocrawlerItem 
from autocrawler.spiders.selectors.sbt_vehicle_details import sbt_vehicle_details_selectors as vehicle_selector
from autocrawler.spiders.selectors.sbt_vehicle_images import VehicleImages as image_selector
class SbtSpider(scrapy.Spider):
    name = 'sbt'
    allowed_domains = ['sbtjapan.com']
    start_urls = ['http://www.sbtjapan.com/used-cars/?t_country=tanzania']

    """
        Initial parse method called when the requests returns
        grab the urls to crawl and then go to product details pages 
    """
    def parse(self, response):
        sel = Selector(response=response)

        vehicle_type_table = sel.xpath('//*[@id="listbox"]/div[4]/ul')
        list_items = vehicle_type_table.css('.car_listitem')

        for listitem in list_items:
            item_link = listitem.css('div.caritem_titlearea > h2 > a::attr(href)').extract()
            log.info("Extracted link : {0}".format(item_link[0]))
            yield scrapy.Request(item_link[0], callback=self.parse_product_detail)
        

    def parse_product_detail(self, response): 
     
        sel = Selector(response=response)
        vehicle = AutocrawlerItem

        vd = vehicle_selector(response)
        vehicle.id = vd.data('id')
        vehicle.vehicle_make = vd.data('make')
        vehicle.vehicle_model = vd.data('model')
        vehicle.vehicle_year = vd.data('year')
        vehicle.vehicle_engine = vd.data('engine')
        vehicle.vehicle_transmission = vd.data('transmission')
        vehicle.vehicle_fuel = vd.data('fuel')
        vehicle.vehicle_seats = vd.data('seats')
        vehicle.vehicle_price_fob = vd.data('price_fob')
        vehicle.vehicle_price_cif = vd.data('price_cif')
        vehicle.vehicle_description = vd.data('description')
        vehicle.Title = vd.data('title')
        vehicle.vehicle_drive = vd.data('wheel_drive')
        vehicle.vehicle_steering = vd.data('steering')
        vehicle.vehicle_color = vd.data('color')
        vehicle.vehicle_doors = vd.data('doors')
        vehicle.vehicle_body = vd.data('body')
        vehicle.vehicle_mileage = vd.data('mileage')
        vehicle.vehicle_accessories = vd.data('accessories')
   
        log.debug('Vehicle images found at {0}'.format(vd.data('images')))
        request = scrapy.Request(vd.data('images') , self.parse_photos)
        #pass vehicle to the next response handler 
        request.meta['vehicle'] = vehicle
        yield request

    """
    Extracts links of photos belonging to the vehicle
    """
    def parse_photos(self, response): 
        log.debug('Getting photos for {0}'.format(vehicle.id))
        
        vehicle_images = image_selector(response)
        vehicle = response.meta['vehicle']
        photo_links = vehicle_images.data('images')
        vehicle['images'] = photo_links
        yield vehicle

