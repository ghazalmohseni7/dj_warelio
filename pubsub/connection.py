import os
import time
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
    max_retries = 10
    retry_delay = 5  # seconds

    # create connection
    credentials = pika.PlainCredentials(username=username, password=password)

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[RabbitMQ] Attempt {attempt}: Connecting to {host}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, credentials=credentials)
            )
            channel = connection.channel()

            # declare exchange
            channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)

            # declare persistent queue
            channel.queue_declare(queue=queue, durable=True)

            # bind queue to exchange with routing key
            channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

            print("[RabbitMQ] ✅ Connected and setup completed.")
            return connection, channel

        except pika.exceptions.AMQPConnectionError as e:
            print(f"[RabbitMQ] ❌ Connection failed: {e}")
            if attempt == max_retries:
                print("[RabbitMQ] ❌ All retry attempts failed.")
                raise
            time.sleep(retry_delay)

