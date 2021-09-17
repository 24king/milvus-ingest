import getopt
import sys
import json
import random
from json.decoder import JSONDecodeError

import pandas

from kafka import KafkaConsumer
from pymilvus import (
    connections, Collection
)

verbose = False
kafka_topic = 'milvus_ingest'
milvus_collection_name = 'hello_milvus'
milvus_host = 'localhost'
milvus_port = 19530
milvus_ingest_batch = 10
kafka_brokers = ['localhost:9092']
kafka_group = 'milvus-ingest'
kafka_auto_offset_reset = 'earliest'
kafka_consumer_timeout = 2000


def ingest():
    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_brokers,
                             group_id=kafka_group,
                             auto_offset_reset=kafka_auto_offset_reset,
                             enable_auto_commit=False,
                             consumer_timeout_ms=kafka_consumer_timeout)
    if verbose:
        print("the default kafka conf \n", KafkaConsumer.DEFAULT_CONFIG)
    print("the kafka conf consumer", consumer.config)

    milvus = connections.connect(host=milvus_host, port=milvus_port)

    if not milvus.has_collection(milvus_collection_name):
        print("milvus中不存在collection:{}".format(milvus_collection_name))
        return

    milvus.load_collection(milvus_collection_name)
    collection = Collection(milvus_collection_name)
    print(collection.schema)
    print(f"\nGet collection entities...")
    print(collection.num_entities)
    df = pandas.DataFrame(data=None, columns=["count", "random_value", "float_vector"])

    while True:
        try:
            for message in consumer:
                msg = json.loads(message.value.decode())
                print(type(msg))
                df1 = pandas.DataFrame([msg], columns=["count", "random_value", "float_vector"])
                df = df.append(df1, ignore_index=True)
                print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                     message.offset, message.key,
                                                     message.value))
                print(len(df))
                if len(df) >= milvus_ingest_batch:
                    ingestdata(df, collection)
                    consumer.commit()

                if len(df) > 0:
                    print("等待时间超过，consumer_timeout_ms,集合数据入库")
                    ingestdata(df, collection)
                    consumer.commit()
        except (JSONDecodeError, ValueError):
            print("I am error", message)


def ingestdata(df, collection):
    print(df)
    collection.insert(df)
    print(df)
    print(collection.num_entities)
    # 删除dataframe
    df.drop(df.index, inplace=True)


def usage():
    print("""
        ingest data from kafka to milvus
        usage: ingest-kafka [option] topic collection
           --help print current help
        -v --verbose print more information
        -b --bootstrap-server default to localhost:9092 split by comma
        -t --topic kafka topic
        -g --group kafka group
        -h --host milvus host
        -p --port milvus port
        -c --connection milvus connection
    """)


if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:], "vb:g:h:p:t:c:",
                                      ["help", "verbose", "bootstrap-server=", "group=",
                                       "host=", "port=", "topic=", "connection="])
        for name, value in options:
            if name == "--help":
                usage()
                sys.exit()
            elif name in ("-v", "--verbose"):
                verbose = True
            elif name in ("-b", "--bootstrap-server"):
                kafka_brokers = value
            elif name in ("-g", "--group"):
                kafka_group = value
            elif name in ("-t", "--topic"):
                kafka_topic = value
            elif name in ("-c", "--connection"):
                milvus_collection_name = value
            elif name in ("-h", "--host"):
                milvus_host = value
            elif name in ("-p", "--port"):
                milvus_port = value
    except getopt.GetoptError:
        usage()

    if verbose:
        print("the options is: ", options)
        print("the args is: ", args)
    ingest()
