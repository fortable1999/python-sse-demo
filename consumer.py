from kafka import KafkaConsumer
consumer = KafkaConsumer('apache_access_log', bootstrap_servers='localhost:9092')

for msg in consumer:
    print(msg)
