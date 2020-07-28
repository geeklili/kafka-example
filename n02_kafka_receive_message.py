from kafka import KafkaConsumer

BOOTSTRAP_SERVER = 'x.x.x.x:9092'
TEST_TOPIC = 'partopic'
consumer = KafkaConsumer(TEST_TOPIC, bootstrap_servers=[BOOTSTRAP_SERVER])
count = 0
for msg in consumer:
	# message_dict = json.loads(msg.value.decode(encoding="utf-8"))
	msg_body = msg.value.decode(encoding="utf-8")
	count += 1
	print(count, ':', msg_body)
