import json

from kafka import KafkaProducer

KAFKA_SERVER = 'x.x.x.x:9092'
TOPIC = 'partopic'


def send_new_msg(jd_id):
	producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])
	msg_body = {'type': 'new_jd', 'jd_id': jd_id}
	msg = str.encode(json.dumps(msg_body))
	producer.send(TOPIC, msg)
	producer.close()


if __name__ == '__main__':
	send_new_msg('abcdefg')
