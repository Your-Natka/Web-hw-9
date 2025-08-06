# pylint: disable=no-member

import pika
import json
import time
import traceback
from mongoengine import connect
from db.models import Contact
from bson import ObjectId
import os

connect(db="contacts_db", host=f"mongodb://{os.getenv('MONGODB_HOST')}:27017", alias="default")

def send_sms_stub(contact: Contact):
    print(f"📲 Надсилаємо SMS до {contact.phone} ({contact.fullname})...")
    contact.is_sent = True
    contact.save()

def callback(ch, method, _, body):
    try:
        print("📨 Отримано повідомлення з sms_queue")
        data = json.loads(body)
        print(f"📦 Дані з повідомлення: {data}")

        contact = Contact.objects(id=ObjectId(data["id"])).first()

        if contact:
            print(f"👤 Знайдено контакт: {contact.fullname}, метод: {contact.send_method}, is_sent: {contact.is_sent}")
            if contact.send_method == "sms" and not contact.is_sent:
                send_sms_stub(contact)
            else:
                print("ℹ️ Контакт уже оброблений або метод не 'sms'")
        else:
            print("⚠️ Контакт не знайдено в базі")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"❌ Помилка під час обробки повідомлення: {e}")
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
