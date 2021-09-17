import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
topic = 'milvus_out'


def test():
    print('begin')
    n = 1
    try:
        while n <= 100:
            producer.send(topic, str(n).encode())
            print("send" + str(n))
            n += 1
            time.sleep(0.5)
    except KafkaError as e:
        print(e)
    finally:
        producer.close()
        print('done')


def test_json():
    msg_dict = {
        "sleep_time": 10,
        "db_config": {
            "database": "test_1",
            "host": "limix",
            "user": "root",
            "password": "root"
        },
        "table": "msg",
        "msg": "Hello World"
    }
    msg = json.dumps(msg_dict)
    producer.send(topic, msg, partition=0)
    producer.close()


if __name__ == '__main__':
    test()
