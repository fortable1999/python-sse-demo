import sys
from urllib import parse
import os
import json
import asyncio
from typing import Optional

from quart import jsonify, Quart, render_template, request
from quart.exceptions import BadRequest

import kafka
from aiokafka import AIOKafkaConsumer
import asyncio

KAFKA_HOSTS = os.environ.get('KAFKA_HOSTS', 'kafka:9092')
app = Quart(__name__)
app.clients = set()

class ServerSentEvent:
    """
    SSE format
    """

    def __init__(
            self,
            data: str,
            *,
            event: Optional[str]=None,
            id: Optional[int]=None,
            retry: Optional[int]=None,
    ) -> None:
        self.data = data
        self.event = event
        self.id = id
        self.retry = retry

    def encode(self) -> bytes:
        message = f"data: {self.data}"
        if self.event is not None:
            message = f"{message}\nevent: {self.event}"
        if self.id is not None:
            message = f"{message}\nid: {self.id}"
        if self.retry is not None:
            message = f"{message}\nretry: {self.retry}"
        message = f"{message}\r\n\r\n"
        result = message.encode('utf-8')
        return result


@app.route('/', methods=['GET'])
async def index():
    consumer = kafka.KafkaConsumer(bootstrap_servers=KAFKA_HOSTS)
    topics = consumer.topics()
    return await render_template('index.html', topics=topics)


@app.route('/sse')
async def sse():
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(loop=loop, bootstrap_servers=KAFKA_HOSTS)
    
    # wait for kafka ready, retry 10 ties
    for i in range(10):
        try:
            await consumer.start()
            break
        except:
            await asyncio.sleep(3)
    else:
        raise BadRequest()

    query = dict(parse.parse_qsl(request.query_string))
    if 'topics' in query:
        consumer.subscribe(topics=query['topics'].split(','))
    else:
        consumer.subscribe(pattern='access_log-.*')

    async def send_events():
        try:
            async for msg in consumer:
                # push to clients
                message = json.loads(msg.value).get('message', "NONE")
                data = "%s > %s" % (msg.topic, message)
                event = ServerSentEvent(data)
                yield event.encode()
        finally:
            # due to bug: https://github.com/aio-libs/aiokafka/issues/252
            await consumer.stop()

    return send_events(), {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Transfer-Encoding': 'chunked',
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0')
