import os
import json
import pika
from dotenv import load_dotenv
from pubsub.connection import rabbitmq_connection

load_dotenv()


def publish(message: dict):
    try:
        exchange = os.getenv("RABBIT_EXCHANGE_NAME")
        routing_key = os.getenv("RABBIT_ROUTING_KEY")
        connection, channel = rabbitmq_connection()

        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message).encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        print(f"✅ Message {message} published on routing key '{routing_key}'")
    except Exception as e:
        print(f"❌ Failed to publish message: {e}")