from scrapy.selector import Selector
import logging 
log = logging.getLogger()

class VehicleImages: 
    def __init__(self, response):
        self.sel = Selector(response=response) 
        self.vehicle = self.select_items()
    
    def select_items(self):
        vehicle = {}
        vehicle['images'] = []
        photos = self.sel.xpath('//*[@id="container"]/div[2]/div')
        photo_links = photos.css('a::attr(href)')

        for p in photo_links: 
           vehicle['images'].append(p.extract())
        return vehicle 

    def data(self, item):
        return self.vehicle[item]
