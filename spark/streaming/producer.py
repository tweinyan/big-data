import json

class Kafka_producer():
    '''
    使用kafka的生产模块
    '''
    def __init__(self, kafkahost, kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
        ))

    def sendjsondata(self, params):
        try:
            params_message = json.dumps(params)
            producer = self.producer
            future = producer.send(topic=self.kafkatopic, value=params_message.encode('utf-8'))
            record_metadata = future.get(timeout=10)
            producer.flush()
            print("-"*50)
            print("topic : {0}".format(record_metadata.topic))
            print("partition : {0}".format(record_metadata.partition))
            print("offset : {0}".format(record_metadata.offset))
            print(params_message)
        #except ValueError:
        except RuntimeError as e:
            print(e)
            print('----')
        #except KafkaError as e:
        #    print(e)

import time

def main():
    '''
    测试consumer和producer
    :return
    '''
    ## 测试生产模块
    producer = Kafka_producer("127.0.0.1", 9092, "test6")
    for i in range(60):
        params = 'pyspark, kafka-streaming, zhang, xiao ming,'
        producer.sendjsondata(params)
        time.sleep(1)

if __name__ == "__main__":
    main()
