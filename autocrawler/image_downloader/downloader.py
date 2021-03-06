import requests
import logging
import shutil
import sys
import json
import os
from message_queue import MessageQueue

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)


def get_filename(url):
    url_parts = url.split('/')
    filename = ''
    if len(url_parts) > 0:
        filename = url_parts[-1]
    # replace some characters we dont need
    file_parts = filename.split('?')
    return file_parts[-2]


def get_dir(url):
    url_parts = url.split('/')
    return url_parts[-2]


def process_message(channel, method_frame, header_frame, body):
    """ Processes received message by downloading files and then publishes it to the next queue for indexing """
    message_string = str(body, 'utf-8')
    msg = json.loads(message_string)

    if len(msg.get('vehicle_thumbnails')) > 0:
        image_file_paths = process_links(msg.get('vehicle_thumbnails'))
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        log.info("Sending ack %s", method_frame.delivery_tag)
        # publish back on to the indexing queue
        msg.vehicle_images = image_file_paths
        publish(msg)

def publish(message):
    """ Publish message to the indexing queue """ 
    EXCHANGE = "crawler.vehicles"
    QUEUE = "indexer_queue"
    q = MessageQueue(EXCHANGE, QUEUE)
    ROUTING_KEY = "indexer.index"
    q.publish(ROUTING_KEY, message)

def process_links(url_list):
    images = []
    for l in url_list:
        dirpath = '/tmp/' + get_dir(l) + "/"
        filepath = dirpath + get_filename(l)

        # TODO: check if the filename already exists on disk and skip if yes
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        log.info("Processing url: %s", l)
        images.append(download(l, filepath))
    return images

def download(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    log.info("Downloaded file %s", file_path)
    return file_path
