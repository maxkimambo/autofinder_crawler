# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import logging 
log = logging.getLogger()
from autocrawler.items import AutocrawlerItem 
from autocrawler.spiders.selectors.sbt_vehicle_details import sbt_vehicle_details_selectors as vehicle_selector

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
        log.debug('---------------')
        vehicle.vehicle_ref_no = vd.data('id')
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

        log.debug('Model {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]/text()').extract()))
        log.debug('Year {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[2]/td[1]/text()').extract()))
        log.debug('Engine {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[7]/td[1]/text()').extract()))
        log.debug('Transmission {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[3]/td[1]/text()').extract()))
        log.debug('Fuel  {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[9]/td[1]/text()').extract()))
        log.debug('Seats {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[2]/text()').extract()))
        log.debug('Price fob : {0}'.format(sel.xpath('//*[@id="fob"]/text()').extract()))
        log.debug('Price cif: {0}'.format('N/A'))
        log.debug('Description {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/p/text()').extract()))
        log.debug('Title {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/h1/text()').extract()))
        log.debug('Drive  {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[4]/td[1]/text()').extract()))
        log.debug('Steering : {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[1]/text()').extract()))
        log.debug('Color : {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/text()').extract()))
        log.debug('Doors : {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]/text()').extract()))
        log.debug('Seats : {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[2]/text()').extract()))
        log.debug('Body : {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[6]/td[2]/text()').extract()))
        log.debug('Mileage : {0}'.format(sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[7]/td[2]/text()').extract()))
        
        accesories_table = sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[3]/tbody')
        for row in accesories_table.css('td:not(.back)'):
            log.debug(row.extract())

        #images 
        photobox = sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[1]/div/p')
        photobox_url = photobox.css('a:first-child::attr(href)').extract()
       
        log.debug('Vehicle images found at {0}'.format(photobox_url[0]))
        request = scrapy.Request(photobox_url[0], self.parse_photos)
        request.meta['vehicle_id'] = sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/text()').extract()
        yield request

    """
    Extracts links of photos belonging to the vehicle
    """
    def parse_photos(self, response): 
       
        log.debug('Getting photos for {0}'.format(response.meta['vehicle_id']))
        sel = Selector(response=response)

        photos = sel.xpath('//*[@id="container"]/div[2]/div')
        photo_links = photos.css('a::attr(href)')

        for p in photo_links: 
            log.debug(p.extract())
        pass 
  