import json

import pika

credentials = pika.PlainCredentials(username='user',
                                    password='password')
print(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                               port=5672,
                                                               credentials=credentials))
channel = connection.channel()

# Declare the exchange
exchange_name = 'my_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

# Send a message to the exchange
for i in range(1):
    message = f'Hello, World! {i}'
    data = {"sender": "Python", "message": message}
    channel.basic_publish(exchange=exchange_name, routing_key='', body=json.dumps(data).encode())

print("Sent message '%s'" % message)

connection.close()

