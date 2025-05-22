import os
import json
import pika
import requests
from dotenv import load_dotenv
from pubsub.connection import rabbitmq_connection

load_dotenv()


def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode('utf-8'))
        print(f"📥 Received message: {message}")

        # send request to inventoy.get
        url_inventory_get = f'http://127.0.0.1:8000/inventoryvs/inventoryvs/?warehouse__id={message["warehouse_id"]}'
        print('qqqqqqqqqqqq', url_inventory_get)
        # send request for approval

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("✅ Message acknowledged")

    except json.JSONDecodeError as e:
        print(f"❌ Failed to decode message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Drop the message

    except Exception as e:
        print(f"❌ Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Requeue for retry


def subscribe():
    connection, channel = rabbitmq_connection()
    queue = os.getenv("RABBIT_QUEUE")
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
    print(f"Waiting for messages on queue '{queue}'.")
    channel.start_consuming()


if __name__ == "__main__":
    subscribe()
