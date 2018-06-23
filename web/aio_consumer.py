from aiokafka import AIOKafkaConsumer
import asyncio

loop = asyncio.get_event_loop()

async def consume():
    consumer = AIOKafkaConsumer(
        'apache_access_log',
        loop=loop, bootstrap_servers='kafka:9092')
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        print("wait")
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

loop.run_until_complete(consume())