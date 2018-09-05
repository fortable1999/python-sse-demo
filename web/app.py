import os
import kafka
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, jsonify

from search import search_by_querystr, histogram_by_topic


KAFKA_HOSTS = os.environ.get('KAFKA_HOSTS', 'localhost:9092')
app = Flask(__name__)
app.clients = set()


@app.route('/', methods=['GET'])
def stream():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    return render_template('stream.html', topics=topics)

@app.route('/search', methods=['GET'])
def search():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    q_str = request.args.get('query', '')
    logs = search_by_querystr(q_str)
    return render_template('search.html', topics=topics, logs=logs)

@app.route('/diagram', methods=['GET'])
def diagram():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    return render_template('diagram.html', topics=topics)

@app.route('/histogram', methods=['GET'])
def histogram():
    topic = request.args.get('topic', '')
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    interval = request.args.get('interval', '5s')
    data = histogram_by_topic(topic, start, end, interval)
    return jsonify(
        data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
