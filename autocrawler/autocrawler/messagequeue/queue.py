import autocrawler.config as config 
import pika 
import os 
import logging
import json

log = logging.getLogger(__name__)

class Queue(object): 
    
    EXCHANGE = config.params.get('exchange')
    EXCHANGE_TYPE = config.params.get('exchange_type')
    QUEUE = config.params.get('crawler_queue')
    ROUTING_KEY = config.params.get('routing_key')

    def __init__(self): 
       
        self._connection = None
        self._channel = None
        self._url = config.get_url()
        self._stopping = False
        self._closing = False
        self.initialise()
        

    def initialise(self):
        log.info('Initialising queues')
        url = config.get_url()
        params = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.QUEUE)
        log.info('Initialisation complete')

    def publish(self, message): 
        log.info('Publishing a message')
        self._channel.basic_publish(self.EXCHANGE,
                                    self.ROUTING_KEY,
                                    json.dumps(dict(message), ensure_ascii=False))
        log.info('message sent')
         
    