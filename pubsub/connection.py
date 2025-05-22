import os
from functools import lru_cache
import pika

from pika.adapters.blocking_connection import BlockingChannel


@lru_cache
def rabbitmq_connection() -> BlockingChannel:
    host = os.getenv("RABBIT_HOST")
    exchange_type = os.getenv("RABBIT_EXCHANGE_TYPE")
    exchange = os.getenv("RABBIT_EXCHANGE_NAME")
    queue = os.getenv("RABBIT_QUEUE")
    routing_key = os.getenv("RABBIT_ROUTING_KEY")
    # create connection
    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params=connection_params)
    # declare channel
    channel = connection.channel()
    # declare exchange
    channel.exchange_declare(exchange_type=exchange_type, exchange=exchange, durable=True)

    # declare persistemt queue
    channel.queue_declare(queue=queue, durable=True)

    # bind queue , exchange with routing key
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    return channel
