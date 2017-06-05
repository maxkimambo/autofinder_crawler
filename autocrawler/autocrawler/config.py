import os 

try:
    BROKER_HOST = os.environ['BROKER_HOST']
except KeyError:
    BROKER_HOST = 'mq'

try:
    BROKER_PORT = os.environ['BROKER_PORT']
except KeyError:
    BROKER_PORT = 5672

try:
    BROKER_USERID = os.environ['BROKER_USERID']
except KeyError:
    BROKER_USERID = 'guest'

try:
    BROKER_PASSWORD = os.environ['BROKER_PASSWORD']
except KeyError:
    BROKER_PASSWORD = 'guest'

try:
    BROKER_VIRTUAL_HOST = os.environ['BROKER_VIRTUAL_HOST']
except KeyError:
    BROKER_VIRTUAL_HOST = '/' 
params={
    'exchange': '',
    'exchange_type': 'topic',
    'routing_key': 'crawler',
    'crawler_queue': 'crawler'
}
def get_url(): 
    url = 'amqp://{0}:{1}@{2}:{3}/%2F'.format(BROKER_USERID, BROKER_PASSWORD, BROKER_HOST, BROKER_PORT)
    return url



