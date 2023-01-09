import pika

credentials = pika.PlainCredentials(username='user',
                                    password='password')

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

# Declare the exchange
exchange_name = 'my_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')


# Declare an exclusive, auto-delete queue and bind it to the exchange
result = channel.queue_declare(queue='', durable=False, exclusive=True, auto_delete=True)
queue_name = result.method.queue
channel.queue_bind(exchange=exchange_name, queue=queue_name)


# Define a callback function to process incoming messages
def on_message(channel, method_frame, header_frame, body):
    print("Received message: %s" % body)


# Set up a consumer and start reading messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
channel.start_consuming()
