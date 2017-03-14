import pika

def on_open(connection):
    print("Connection activated")

connection = pika.SelectConnection(on_open_callback=on_open)
