from threading import Thread
from .consumer import create_consumer, consume_messages

def init_kafka():
    consumer = create_consumer()
    thread = Thread(target=consume_messages, args=(consumer,))
    thread.daemon = True
    thread.start()