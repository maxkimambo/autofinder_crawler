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
        
        log.info('[Queue] Initialising queues')
        url = config.get_url()
        params = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(params)
        log.info('[Queue] Connection established')
        self._channel = self._connection.channel()
        log.info('[Queue] Channel created')
        log.info('[Queue] Setting up Exchange %s of type %s', self.EXCHANGE, self.EXCHANGE_TYPE)
        self._channel.exchange_declare(exchange=self.EXCHANGE, type=self.EXCHANGE_TYPE)
        log.info('[Queue] Finished setting up Exchange %s of type %s', self.EXCHANGE, self.EXCHANGE_TYPE)
        # self._channel.queue_declare(queue=self.QUEUE, durable=True, exclusive=False, auto_delete=False)
        log.info('[Queue] Initialisation complete')

    def publish(self, message): 
        
        self._channel.basic_publish(exchange=self.EXCHANGE,
                                    routing_key=self.ROUTING_KEY,
                                    body=json.dumps(dict(message), ensure_ascii=False), 
                                    properties=pika.BasicProperties(content_type='application/json',
                                                         delivery_mode=1))
    def disconnect(self): 
        log.info('[Disconnect] Closing connection ')
        self._connection.close()
    
         
    