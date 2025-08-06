# pyright: reportMissingImports=false

import pika
import json

# Параметри підключення
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Назва черги (переконайся, що консьюмер слухає цю саму чергу)
queue_name = 'email_queue'

# Тестове повідомлення
message = {
    "fullname": "Test User",
    "email": "test@example.com",
    "send_method": "email"
}

# Відправка
channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body=json.dumps(message),
)

print(f"✅ Повідомлення надіслано в чергу {queue_name}")

# Закрити з'єднання
connection.close()