#   Vehicle Id: = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/text()').extract()
#         Make = self.sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/h1/text()').extract()
#         Model = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]/text()').extract()
#         Year = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[2]/td[1]/text()').extract()
#         Engine = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[7]/td[1]/text()').extract()
#         Transmission = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[3]/td[1]/text()').extract()
#         Fuel  = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[9]/td[1]/text()').extract()
#         Seats = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[2]/text()').extract()
#         Price fob : = self.sel.xpath('//*[@id="fob"]/text()').extract()
#         Price cif: {0}'.format('N/A'))
#         Description = self.sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/p/text()').extract()
#         Title = self.sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/h1/text()').extract()
#         Drive  = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[4]/td[1]/text()').extract()
#         Steering : = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[1]/text()').extract()
#         Color : = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/text()').extract()
#         Doors : = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]/text()').extract()
#         Seats : = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[2]/text()').extract()
#         Body : = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[6]/td[2]/text()').extract()
#         Mileage : = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[7]/td[2]/text()').extract()
from scrapy.selector import Selector
import logging 
log = logging.getLogger()

class sbt_vehicle_details_selectors: 
    

    def __init__(self, response):
        self.sel = Selector(response=response) 
        self.vehicle = self.select_items()

    def select_items(self): 
        # return a hash of values 
        vehicle = {}
        vehicle['id'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/text()').extract()
        vehicle['make'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/h1/text()').extract()
        vehicle['model'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]/text()').extract()
        vehicle['year'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[2]/td[1]/text()').extract()
        vehicle['engine'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[7]/td[1]/text()').extract()
        vehicle['transmission'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[3]/td[1]/text()').extract()
        vehicle['fuel']  = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[9]/td[1]/text()').extract()
        vehicle['seats'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[2]/text()').extract()
        vehicle['price_fob'] = self.sel.xpath('//*[@id="fob"]/text()').extract()
        vehicle['price_cif'] = 'N/A'
        vehicle['description']= self.sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/p/text()').extract()
        vehicle['title'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/ul/li[2]/h1/text()').extract()
        vehicle['wheel_drive']  = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[4]/td[1]/text()').extract()
        vehicle['steering']  = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[5]/td[1]/text()').extract()
        vehicle['color'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/text()').extract()
        vehicle['doors'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]/text()').extract()
        vehicle['body'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[6]/td[2]/text()').extract()
        vehicle['mileage'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[7]/td[2]/text()').extract()
        return vehicle; 
    
    def data(self, item):
        return self.vehicle[item][0]
