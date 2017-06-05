# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
log = logging.getLogger()
from autocrawler.messagequeue.queue import Queue 
class AutocrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class MessageQueuePipeline(object): 
   
    def __init__(self): 
        self.queue = Queue()

    def spider_opened(self, spider): 
        log.info('Spider opened')
        pass
       
    def spider_closed(self, spider): 
        # clean up the queues 
        log.info('Spider closed')
        # self.queue.disconnect()
    
    def process_item(self, item, spider): 
        # log.debug('MessageQueuePipeline: item {0}'.format(json.dumps(dict(item))))
        self.queue.publish(item)
        return item
