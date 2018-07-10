import os

from quart import Quart, render_template

import kafka

KAFKA_HOSTS = os.environ.get('KAFKA_HOSTS', 'localhost:9092')
app = Quart(__name__)
app.clients = set()


@app.route('/', methods=['GET'])
async def index():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    return await render_template('index.html', topics=topics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
