import pika
import os
import logging
import json
import sys
import re
# import hashlib

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)


class MessageQueue(object):
    """
    MessageQueue class connects and publishes messages to the broker 
        :param object: 
    """
    EXCHANGE = os.getenv('EXCHANGE', 'crawler.vehicles')
    QUEUE = os.getenv('QUEUE', 'crawler_queue')
    EXCHANGE_TYPE = 'topic'

    def __init__(self):

        self._connection = None
        self._channel = None

        self._stopping = False
        self._closing = False
        self._userId = os.getenv('BROKER_USERID', 'guest')
        self._password = os.getenv('BROKER_PASSWORD', 'guest')
        self._broker_host = os.getenv('BROKER_HOST', 'guest')
        self._broker_port = os.getenv('BROKER_PORT', 5672)

        self.initialise()

    def get_url(self):
        """
        Generates connection string
        """
        url = 'amqp://{0}:{1}@{2}:{3}/%2F'.format(
            self._userId, self._password, self._broker_host, self._broker_port)
        return url

    def initialise(self):
        """
        Initialises RabbitMQ connection and queues
        """
        log.info('---- Initialising queue ----')
        url = self.get_url()
        params = pika.URLParameters(url)
        self._connection = pika.BlockingConnection(params)
        log.info('Connection established')

        self._channel = self._connection.channel()
        log.info('Channel created')

        log.info('Setting up Exchange %s of type %s',
                 self.EXCHANGE, self.EXCHANGE_TYPE)
        self._channel.exchange_declare(
            exchange=self.EXCHANGE, exchange_type=self.EXCHANGE_TYPE)
        self._channel.queue_declare(
            queue=self.QUEUE, durable=True, exclusive=False, auto_delete=False)
        log.info('Declared queue %s ', self.QUEUE)

        log.info('Initialisation complete')

    def publish(self, message):
        """
        publishes message to the queue
        """
        try:
            
            log.debug('----------- Publishing messsage ---------------')
            log.debug(message)
            log.debug('------------------ END ------------------------ \r\n')

            payload = json.dumps(dict(message), ensure_ascii=False)
  
            # #add the checksum 
            # md5 = hashlib.md5()
            # md5.update(payload)
            # # md5.update(repr(vehicle))
            # payload["checksum"] = md5.hexdigest()

            self._channel.basic_publish(exchange=self.EXCHANGE,
                                        routing_key='crawler_output.*',
                                        body=payload,
                                        properties=pika.BasicProperties(content_type='application/json',
                                                                        delivery_mode=1))
        except TypeError as te:
            log.error('Unserializable message found %s', message)

    def disconnect(self):
        """
        Disconnects from the queue
        """
        log.info('[Disconnect] Closing connection ')
        self._connection.close()