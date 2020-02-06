#!/usr/bin/env python
from kafka import KafkaProducer
import time

KAFKA_VERSION = (2, 4)
# producer = KafkaProducer(bootstrap_servers=['localhost:38887'], value_serializer=lambda x: json.dumps(x).encode('utf-8'), api_version=KAFKA_VERSION)
# producer = KafkaProducer(bootstrap_servers=['localhost:38887'],  api_version=KAFKA_VERSION)
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],  api_version=KAFKA_VERSION)

while True:
    msg = "123"
    print("sending msg")
    producer.send('test', value=msg)
    time.sleep(1)
