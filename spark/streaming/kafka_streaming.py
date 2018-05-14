ssc = StreamingContext(sc, 10)
kafka_stream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": "localhost:9092"})
lines = kafka_stream.map(lambda x: x[1])
lines.pprint()
