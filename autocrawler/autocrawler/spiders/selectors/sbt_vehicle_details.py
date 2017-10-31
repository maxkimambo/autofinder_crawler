from scrapy.selector import Selector
import logging 
import sys

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)

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
        vehicle['year'] = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]/text()').extract()
                                         #//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]
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
        
        # accessories 
        accesories_table = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[2]/table[3]/tbody')
        accessories = []
        for row in accesories_table.css('td:not(.back)'):
            accessories.append(row.extract())
        vehicle['accessories'] = accessories
    
        # images url 
        photobox = self.sel.xpath('//*[@id="contents_detail"]/div[3]/div[1]/div[1]/div/p')
        photobox_url = photobox.css('a:first-child::attr(href)').extract()
       
        vehicle['images'] = photobox_url
        return vehicle; 
    
    def get(self, item):
            
        try: 
            result = self.vehicle[item][0]
           
            return result
        except IndexError as err: 
            log.error('Failed to get item: %s of vehicle id : %s', item, self.vehicle.get("id"))
            result = '' # set to empty value
            return result
