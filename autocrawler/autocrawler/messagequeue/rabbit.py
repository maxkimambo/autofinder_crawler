# Ref: https://pika.readthedocs.io/en/0.10.0/examples/asynchronous_publisher_example.html

import autocrawler.config as config 
import pika 
import os 
import logging
import json

log = logging.getLogger(__name__)

class Rabbit(object):
    
    EXCHANGE = config.params.get('exchange')
    EXCHANGE_TYPE = config.params.get('exchange_type')
    QUEUE = config.params.get('crawler_queue')
    ROUTING_KEY = config.params.get('routing_key')

    def __init__(self): 
        # init pika
        self._connection = None
        self._channel = None
        self._url = config.get_url()
        self._stopping = False
        self._closing = False
        self.initialize()
        


    def initialize(self): 
        print('initialising')
        log.info('initialising')
        if not self._connection :
            log.info('[Queue Setup] No connection found initalizing..')
            self._connection = self.connect()
            self._connection.ioloop.start()
        
    def connect(self):
        log.info('[Queue Setup] CONNECTING TO %s ', self._url)
        return pika.SelectConnection(pika.URLParameters(self._url), 
                                    self.on_connection_open, 
                                    stop_ioloop_on_close=False)

    def disconnect(self): 
        log.info('[Queue Setup] Disconnecting from Queue ')
        self._stopping = True
        self.close_channel()
        self.close_connection()
        self._connection.ioloop.start()
        log.info('[Queue] Gracefully disconnected')

    def on_connection_open(self, connection): 
        log.info('[Queue Setup] Connection established')
        self.add_on_connection_close_callback()
        self.open_channel()
    
    def add_on_connection_close_callback(self): 
        log.info('[Queue Setup] Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self): 
        """
        Here we can setup reconnection logic if connection is lost unexpectedly 
        """
        self._channel = None 
        if self._closing: 
            self._connection.ioloop.stop()
        else: 
            log.warning('[Queue Setup] Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self): 
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()
        # Create a new connection
        # self._connection = self.connect()
        # # There is now a new connection, needs a new ioloop to run
        # self._connection.ioloop.start()

    def open_channel(self):
        log.info('[Queue Setup] Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel): 
        log.info('[Queue Setup] Channel openned')
        
    def on_open(self, connection):
        log.info('[Queue Setup] Setting up connection')
        connection.channel(on_channel_open)
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        log.info('[Queue Setup] Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text): 
        log.warning('[Queue Setup] Channel was closed: (%s) %s', reply_code, reply_text)
        if not self._closing:
            self._connection.close()

    def setup_exchange(self, exchange_name): 
        log.info('[Queue Setup] Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(self.on_exchange_declared, exchange_name, self.EXCHANGE_TYPE)

    def on_exchange_declared(self, unused_frame): 
        log.info('[Queue Setup] Exchange declared OK')

    def setup_queue(self, queue_name): 
        log.info('[Queue Setup] Setting up queue  %s', queue_name)
        self._channel.queue_declare(self.on_queue_declared, queue_name)
    
    def on_queue_declared(self, method_frame): 
        log.info('[Queue Setup] Queue %s created', queue_name)
        log.info('[Queue Setup] Binding exchange %s to queue %s with routing key $s', 
                   self.EXCHANGE, self.QUEUE, self.ROUTING_KEY)

        self._channel.queue_bind(self.on_queue_bound, self.QUEUE,
                                 self.EXCHANGE, self.ROUTING_KEY)
                        
    def on_queue_bound(self, unused): 
        log.info('[Queue Setup] Queue bound')
        log.info('[Queue Setup] Queue setup complete... messsages can be sent now!!')
        # self.start_publishing()

    def publish(self, message):
        """ Called when the producers wants to send the message """ 
       
        properties = pika.BasicProperties(app_id='crawler-publisher', 
                                            content_type='application/json',
                                            headers=message)
        self._channel.basic_publish(self.EXCHANGE,
                                    self.ROUTING_KEY,
                                    json.dumps(message, ensure_ascii=False),
                                     properties)
        # log.debug('[Queue] Published message %s', json.dumps(dict(message)))
        log.debug('[Queue] Published message')
