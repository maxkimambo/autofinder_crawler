# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class AutocrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object): 
    def __init__(self): 
        self.file = open('crawler_data.json', 'wb')

    def process_item(self,item, spider): 
        print('PIPELINE ===> ')
        print('data: '.format(item))
        # # with open('crawler_data.json', 'w') as outfile: 
        # #     json.dump(dict(item),sort_keys=True, indent=4)
        # line = json.dumps(dict(item))
        # self.file.write(line)
        # return item
        return item 