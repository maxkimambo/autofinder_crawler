FROM python:3.4.6-wheezy
MAINTAINER Max Kimambo, max@kimambo.de 

RUN pip3 install scrapy pika

VOLUME "/var/app"

CMD ["bash"]