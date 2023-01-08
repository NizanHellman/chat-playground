import pika

credentials = pika.PlainCredentials(username='user',
                                    password='password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.250.22',
                                                               port=5672,
                                                               credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello', auto_delete=True)

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [X] Sent 'hello World!'")

connection.close()

