import json

from kafka import KafkaConsumer

topic = 'milvus_in'
consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])


def consumer_demo():
    for message in consumer:
        print("receive, key:{}, value:{}".format(
            json.loads(message.key.decode()),
            json.loads(message.value.decode())
        ))


if __name__ == '__main__':
    consumer_demo()
