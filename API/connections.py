from typing import Optional
from redis import Redis
from API import redis_url

class RedisCache:
    def __init__(self):
        self.redis_cache = None

    def init_cache(self, redis_url):
        self.redis_cache = Redis.from_url(redis_url, decode_responses=True)

    async def set(self, key, value):
        return await self.redis_cache.set(key, value)

    async def get(self, key):
        return await self.redis_cache.get(key)

    async def set_expire(self, key, value, time=900):
        return await self.redis_cache.execute_command("set", key, value, "ex", time)

    async def flush_db(self):
        await self.redis_cache.flushdb()

    async def close(self):
        await self.redis_cache.close()


redis_cache = RedisCache()
