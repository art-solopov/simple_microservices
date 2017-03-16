import pika


# Global channel variable
channel = None
queue = 'test'


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


def handle_delivery(channel, method, header, body):
    print(body)


conn_params = pika.ConnectionParameters()
connection = pika.SelectConnection(conn_params, on_connected)

if __name__ == '__main__':
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()
