# pyright: reportMissingImports=false

import pika
import json
import time
import traceback
from mongoengine import connect
from db.models import Contact
import os

# Підключення до MongoDB
connect(
    db="contacts_db",
    host=f"mongodb://{os.getenv('MONGODB_HOST')}:27017",
    alias="default"
)

def callback(ch, method, _, body):
    try:
        data = json.loads(body)
        contact_id = data.get("id")
        contact = Contact.objects(id=contact_id).first()

        if contact and contact.send_method == "sms":
            print(f"📲 Надсилаємо SMS до {contact.phone} ({contact.fullname})...")
            contact.is_sent = True
            contact.save()
        else:
            print(f"⚠️ Контакт {contact_id} не знайдено або спосіб не SMS")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"❌ Помилка під час обробки sms: {e}")
        traceback.print_exc()
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Очікуємо RabbitMQ
for _ in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        break
    except pika.exceptions.AMQPConnectionError:
        print("⏳ Очікуємо RabbitMQ...")
        time.sleep(5)
else:
    print("❌ RabbitMQ недоступний. Завершення.")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue="sms_queue")
channel.basic_consume(queue="sms_queue", on_message_callback=callback)

print("📥 Очікуємо SMS-повідомлення...")
channel.start_consuming()
