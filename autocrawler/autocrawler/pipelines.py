# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import sys

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)
from autocrawler.messagequeue.queue import MessageQueue 
class AutocrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class MessageQueuePipeline(object): 
   
    def __init__(self): 
        self.queue = MessageQueue()

    def spider_opened(self, spider): 
        log.info('Spider opened')
        pass
       
    def spider_closed(self, spider): 
        # clean up the queues 
        log.info('Spider closed')
        # self.queue.disconnect()
    
    def process_item(self, item, spider): 
        self.queue.publish(item)
        return item
