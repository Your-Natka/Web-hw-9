# redis_cache.py
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cache(key):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key, data, expire=3600):
    redis_client.set(key, json.dumps(data), ex=expire)
