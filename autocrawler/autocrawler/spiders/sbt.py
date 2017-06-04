# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import copy 
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
        vehicle = AutocrawlerItem()

        vd = vehicle_selector(response)
        vehicle['id'] = vd.get('id')
        vehicle['vehicle_make'] = vd.get('make')
        vehicle['vehicle_model'] = vd.get('model')
        vehicle['vehicle_year'] = vd.get('year')
        vehicle['vehicle_engine'] = vd.get('engine')
        vehicle['vehicle_transmission'] = vd.get('transmission')
        vehicle['vehicle_fuel'] = vd.get('fuel')
        vehicle['vehicle_seats'] = vd.get('seats')
        vehicle['vehicle_price_fob'] = vd.get('price_fob')
        vehicle['vehicle_price_cif'] = vd.get('price_cif')
        vehicle['vehicle_description'] = vd.get('description')
        vehicle['vehicle_title'] = vd.get('title')
        vehicle['vehicle_drive'] = vd.get('wheel_drive')
        vehicle['vehicle_steering'] = vd.get('steering')
        vehicle['vehicle_color'] = vd.get('color')
        vehicle['vehicle_doors'] = vd.get('doors')
        vehicle['vehicle_body'] = vd.get('body')
        vehicle['vehicle_mileage'] = vd.get('mileage')
        vehicle['vehicle_accessories'] = vd.get('accessories')
   
        log.debug('Vehicle images found at {0}'.format(vd.get('images')))
        request = scrapy.Request(vd.get('images') , self.parse_photos)
        #pass vehicle to the next response handler 
        request.meta['vehicle'] = {'data': vehicle}
        yield request

    """
    Extracts links of photos belonging to the vehicle
    """
    def parse_photos(self, response): 

        vehicle_images = image_selector(response)
        # TODO: deal with returning item instead of meta 
        meta = response.meta['vehicle']
        
        vehicle = meta['data'] 
        log.debug( type(vehicle))
        log.debug('Getting photos for {0}'.format(vehicle['id']))
    
        photo_links = vehicle_images.get('images')
        vehicle['vehicle_thumbnails'] = photo_links
        yield vehicle

