import os
import redis





REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None

def normalize_question(q: str) -> str:
    return q.strip().lower()

def get_answer_from_redis(question: str):
    if not redis_client:
        return None
    key = f'rag:{normalize_question(question)}'
    try:
        return redis_client.get(key)
    except Exception:
        return None
    

def set_answer_to_redis(question: str, answer: str, ttl: int=86400):
    if not redis_client:
        return None
    key = f'rag:{normalize_question(question)}'
    try:
        redis_client.setex(key, ttl, answer)
    except Exception:
        pass