import os
import json
import redis
from typing import Optional

class RedisAnswerStore:
    def __init__(self, prefix: str, redis_url: str):
        self.prefix = prefix
        self.redis_url = redis_url or os.getenv("REDIS_URL")
        if not self.redis_url:
            raise ValueError("REDIS_URL is missing")

        self.client = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def key(self, _id: str) -> str:
        return f"{self.prefix}{_id}"

    def get_payload(self, _id: str) -> Optional[dict]:
        raw = self.client.get(self.key(_id))
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    def get_answer(self, _id: str) -> Optional[str]:
        obj = self.get_payload(_id)
        return None if not obj else obj.get("answer")

    def set_payload(self, _id: str, payload: dict) -> bool:
        try:
            self.client.set(self.key(_id), json.dumps(payload, ensure_ascii=False))
            return True
        except Exception as e:
            print("[REDIS SET ERROR]", repr(e))
            return False
