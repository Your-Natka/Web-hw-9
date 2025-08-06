# Web-hw-08

# Контактний мікросервіс з RabbitMQ

## Компоненти
- MongoDB: зберігання контактів
- RabbitMQ: черги для email та sms
- Producer: створює фейкові контакти та надсилає в черги
- Consumers: обробляють email та sms

## Запуск RabbitMQ

```bash
docker-compose up -d