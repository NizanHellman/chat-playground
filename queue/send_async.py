import asyncio
import aio_pika


async def main(loop):
    # Establish a connection to the RabbitMQ server
    connection = await aio_pika.connect_robust(
        "amqp://user:password@localhost:5672/", loop=loop
    )
    async with connection:
        # Open a channel

        channel = await connection.channel()

        # Declare the exchange
        exchange_name = 'my_exchange'
        routing_key = ''
        exchange = await channel.declare_exchange(name=exchange_name, type='fanout')
        await exchange.publish(aio_pika.Message(body='Nivan'.format(routing_key).encode()), routing_key=routing_key)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))
    loop.close()

