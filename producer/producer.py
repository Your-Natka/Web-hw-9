# pylint: disable=no-member

import pika
import time
import json
from faker import Faker
from mongoengine import connect
from db.models import Contact
import os

connect(db="contacts_db", host=f"mongodb://{os.getenv('MONGODB_HOST')}:27017", alias="default")

fake = Faker()

# Підключення до RabbitMQ з повторними спробами
for i in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        channel = connection.channel()  # <--- ДОДАНО
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"RabbitMQ не готовий, спроба {i + 1}/10")
        time.sleep(3)
else:
    print("❌ Не вдалося підключитися до RabbitMQ")
    exit(1)

# Створюємо черги
channel.queue_declare(queue="email_queue")
channel.queue_declare(queue="sms_queue")

# Генеруємо контакти
for _ in range(10):
    method = fake.random_element(["email", "sms"])
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        send_method=method
    ).save()

    message = json.dumps({"id": str(contact.id)})
    queue_name = "email_queue" if method == "email" else "sms_queue"
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)
    print(f"📤 Відправлено контакт {contact.fullname} у чергу {queue_name}")

connection.close()

contact = Contact(
    fullname="Тестовий СМС",
    email="test@example.com",
    phone="+380671234567",
    send_method="sms"
).save()

message = json.dumps({"id": str(contact.id)})
channel.basic_publish(exchange="", routing_key="sms_queue", body=message)
print(f"📤 Відправлено контакт {contact.fullname} у чергу sms_queue")

