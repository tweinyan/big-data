"""
kafka-topics.sh --zookeeper localhost:2181 --list

kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topicname
"""

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def echo(time, rdd):
    pass

if __name__ == '__main__':
    topic = "test3"
    sc = SparkContext(appName="pyspark kafka-streaming")
    ssc = StreamingContext(sc, 10)
    kafka_stream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": "localhost:9092"})

    lines = kafka_stream.map(lambda x: x[1])
    lines.pprint()

    words = lines.flatMap(lambda line: line.split(","))
    words.pprint()

    pairs = words.map(lambda word: (word, 1))
    pairs.pprint()

    counts = pairs.reduceByKey(lambda x, y: x + y)
    counts.pprint()


# spark-submit demo_kafka.py>a.log
