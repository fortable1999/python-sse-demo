import sys
import os
import asyncio
from typing import Optional

from quart import jsonify, Quart, render_template, request

from aiokafka import AIOKafkaConsumer
import asyncio

KAFKA_HOSTS = os.environ.get('KAFKA_HOSTS', 'kafka:9092')

loop = asyncio.get_event_loop()

app = Quart(__name__)
app.clients = set()


async def consume():
    consumer = AIOKafkaConsumer(
        'apache_access_log',
        loop=loop, bootstrap_servers=KAFKA_HOSTS)
    # Get cluster layout and join group `my-group`
    for i in range(10):
        try:
            await consumer.start()
            break
        except:
            print('failed to connect. retry...')
            await asyncio.sleep(3)
    else:
        sys.exit(1)
    try:
        # Consume messages
        print("wait")
        async for msg in consumer:
            for queue in app.clients:
                data = str(("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp))
                await queue.put(data)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


class ServerSentEvent:

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
        return message.encode('utf-8')



@app.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')


@app.route('/', methods=['POST'])
async def broadcast():
    data = await request.get_json()
    for queue in app.clients:
        await queue.put(data['message'])
    return jsonify(True)


@app.route('/sse')
async def sse():
    queue = asyncio.Queue()
    app.clients.add(queue)
    async def send_events():
        while True:
            try:
                data = await queue.get()
                event = ServerSentEvent(data)
                yield event.encode()
            except asyncio.CancelledError as error:
                app.clients.remove(queue)

    return send_events(), {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Transfer-Encoding': 'chunked',
    }

if __name__ == '__main__':
    loop.create_task(consume())
    app.run(host='0.0.0.0', loop=loop)
