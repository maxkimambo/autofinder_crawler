import requests
import logging
import shutil
import sys 
import json 
import os

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)


def get_filename(url):
    url_parts = url.split('/')
    filename = ''
    if len(url_parts) > 0:
        filename = url_parts[-1]
    # replace some characters we dont need
    file_parts= filename.split('?')
    return file_parts[-2]

def get_dir(url):
    url_parts = url.split('/')
    return url_parts[-2]

def process_message(channel, method_frame, header_frame, body):
    message_string = str(body, 'utf-8')
    msg = json.loads(message_string)
    
    if len(msg.get('vehicle_thumbnails')) > 0:
        process_links(msg.get('vehicle_thumbnails'))
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    log.info("Sending ack %s", method_frame.delivery_tag)


def process_links(url_list):
    for l in url_list:
        dirpath = '/tmp/'+ get_dir(l) + "/" 
        filepath = dirpath + get_filename(l)

        #TODO: check if the filename already exists on disk and skip if yes

        if not os.path.exists(dirpath): 
            os.makedirs(dirpath)
        log.info("Processing url: %s", l)
        download(l, filepath)

def download(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    log.info("Downloaded file %s", file_path)
