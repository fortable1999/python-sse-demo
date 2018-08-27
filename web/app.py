import os
import kafka
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

from search import search_by_querystr


KAFKA_HOSTS = os.environ.get('KAFKA_HOSTS', 'localhost:9092')
app = Flask(__name__)
app.clients = set()


@app.route('/', methods=['GET'])
def index():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    return render_template('index.html', topics=topics)

@app.route('/search', methods=['GET'])
def search():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    q_str = request.args.get('query', '')
    logs = search_by_querystr(q_str)
    return render_template('search.html', topics=topics, logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
