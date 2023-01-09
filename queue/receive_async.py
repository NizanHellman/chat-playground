import asyncio
import aio_pika
from aio_pika import connect_robust


async def main(loop):
    connection = await connect_robust(
        "amqp://user:password@localhost:5672/",
        loop=loop
    )

    # queue_name = "test_queue"
    routing_key = ""

    # Creating channel
    channel = await connection.channel()

    # Declaring exchange
    exchange = await channel.declare_exchange(name='my_exchange', type='fanout')

    # Declaring queue
    queue = await channel.declare_queue(auto_delete=True)
    print(f"queue name: {queue.name}")

    # Binding queue
    await queue.bind(exchange, routing_key)

    async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            print(message.body)
            await asyncio.sleep(1)

    # Receiving message
    await queue.consume(callback=process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))
