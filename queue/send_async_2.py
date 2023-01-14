import asyncio
import pika

exchange_name = 'my_exchange'


async def main(loop):

    def get_connection():
        # Establish a connection to the RabbitMQ server
        credentials = pika.PlainCredentials(username='user',
                                            password='password')
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                       port=5672,
                                                                       credentials=credentials))

        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

        return connection, channel

    def publish_msg(connection, channel):
        for i in range(15000):
            message = f'Nivan {i}'
            channel.basic_publish(exchange=exchange_name, routing_key='', body=message.encode())
        connection.close()

    # Declare the exchange
    conn, chan = await loop.run_in_executor(None, get_connection)
    result = await loop.run_in_executor(None, publish_msg, conn, chan)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))
    loop.close()
