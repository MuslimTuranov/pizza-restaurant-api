import json
from typing import Any, Optional
from .redis_config import redis_client

class RedisCache:
    def __init__(self):
        self.client = redis_client
    
    def set(self, key: str, value: Any, expire: int = 3600):
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.client.setex(key, expire, value)
        except Exception as e:
            print(f"Redis set error: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
        except Exception as e:
            print(f"Redis get error: {e}")
        return None
    
    def delete(self, key: str):
        try:
            self.client.delete(key)
        except Exception as e:
            print(f"Redis delete error: {e}")
    
    def delete_pattern(self, pattern: str):
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
        except Exception as e:
            print(f"Redis delete_pattern error: {e}")
    
    def exists(self, key: str) -> bool:
        try:
            return bool(self.client.exists(key))
        except Exception:
            return False

cache = RedisCache()