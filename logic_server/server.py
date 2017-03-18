import pika
import json

from .config import CONFIG
from .actions import registry

# Global channel variable
channel = None
queue = None


def on_connected(connection):
    print("Connection activated")
    connection.channel(on_channel_open)


def on_channel_open(new_channel):
    print("Channel opened")
    global channel
    channel = new_channel
    # TODO: queue params
    channel.queue_declare(
        queue=queue,
        durable=True,
        exclusive=False,
        auto_delete=False,
        callback=on_queue_declared
    )


def on_queue_declared(frame):
    print("Queue {0} declared".format(queue))
    channel.basic_consume(handle_delivery, queue=queue)


def handle_delivery(channel, method, headers, body):
    body = json.loads(body)
    action = body.get('action', None)
    if action is None:
        print("Action is missing")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    result = registry[action](body['data'])        
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if headers.reply_to:
        corr_id = headers.correlation_id
        channel.basic_publish(
            exchange='',
            routing_key=headers.reply_to,
            properties=pika.BasicProperties(
                correlation_id=corr_id,
                content_type='application/json'
            ),
            body=json.dumps(result)
        )


def start():
    conn_params = pika.ConnectionParameters()
    connection = pika.SelectConnection(conn_params, on_connected)
    global queue
    queue = CONFIG['queue']

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()
