# pyright: reportMissingImports=false

import re
import redis
from mongoengine import connect
from db.models import Author, Quote, Tag

# Підключення до MongoDB
connect(
    db="quotes_db",
    host="mongodb+srv://my2sails:RYY9xTGwccokAH6g@cluster0.gp5445y.mongodb.net/quotes_db",
    alias="default"
)

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def print_results(results):
    if not results:
        print("❌ Нічого не знайдено.")
    else:
        for line in results:
            print(line)

def cache_or_fetch(key, fetch_function):
    if redis_client.exists(key):
        print(f"📦 Отримано з кешу: {key}")
        cached = redis_client.lrange(key, 0, -1)
        return cached
    else:
        print(f"🔎 Отримано з MongoDB: {key}")
        results = fetch_function()
        if results:
            redis_client.rpush(key, *results)
        return results

def find_by_author(name_part):
    key = f"name:{name_part.lower()}"

    def fetch():
        regex = re.compile(f'^{re.escape(name_part)}', re.IGNORECASE)
        authors = Author.objects(fullname=regex)
        results = []
        for author in authors:
            quotes = Quote.objects(author=author)
            results.extend([str(q) for q in quotes])
        return results

    results = cache_or_fetch(key, fetch)
    print_results(results)

def find_by_tag(tag_part):
    key = f"tag:{tag_part.lower()}"

    def fetch():
        regex = re.compile(f'^{re.escape(tag_part)}', re.IGNORECASE)
        tags = Tag.objects(name=regex)
        results = []
        for tag in tags:
            quotes = Quote.objects(tags=tag)
            results.extend([str(q) for q in quotes])
        return results

    results = cache_or_fetch(key, fetch)
    print_results(results)

def find_by_tags(tag_list):
    tags = Tag.objects(name__in=tag_list)
    quotes = Quote.objects(tags__in=tags)
    results = [str(q) for q in quotes]
    print_results(results)

if __name__ == "__main__":
    print("🔍 Введіть команду: name:Einstein | tag:life | tags:life,miracle | exit")

    while True:
        user_input = input(">>> ").strip()

        if user_input.lower() == "exit":
            print("👋 Завершення.")
            break

        if ":" not in user_input:
            print("❌ Невірний формат. Використовуйте name:, tag:, tags:")
            continue

        command, value = user_input.split(":", 1)
        value = value.strip()

        if command == "name":
            find_by_author(value)
        elif command == "tag":
            find_by_tag(value)
        elif command == "tags":
            tags = [t.strip() for t in value.split(",")]
            find_by_tags(tags)
        else:
            print("❌ Невідома команда.")
