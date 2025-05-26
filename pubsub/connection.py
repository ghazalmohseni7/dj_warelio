import os
from functools import lru_cache
import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from typing import Tuple


@lru_cache
def rabbitmq_connection() -> Tuple[BlockingConnection, BlockingChannel]:
    host = os.getenv("RABBIT_HOST")
    exchange_type = os.getenv("RABBIT_EXCHANGE_TYPE")
    exchange = os.getenv("RABBIT_EXCHANGE_NAME")
    queue = os.getenv("RABBIT_QUEUE")
    routing_key = os.getenv("RABBIT_ROUTING_KEY")
    username = os.getenv("RABBIT_USERNAME")
    password = os.getenv("RABBIT_password")

    # create connection
    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))

    # declare channel
    channel = connection.channel()

    # declare exchange
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)

    # declare persistemt queue
    channel.queue_declare(queue=queue, durable=True)

    # bind queue , exchange with routing key
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    return connection, channel
