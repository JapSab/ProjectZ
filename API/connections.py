import os
from redis import Redis


class RedisCache:
    def __init__(self, redis_url):
        self.redis_cache = Redis.from_url(redis_url, decode_responses=True)

    async def set(self, key, value):
        if self.redis_cache is None:
            raise RuntimeError("Redis cache is not initialized")
        return await self.redis_cache.set(key, value)

    async def get(self, key):
        if self.redis_cache is None:
            raise RuntimeError("Redis cache is not initialized")
        return await self.redis_cache.get(key)

    async def set_expire(self, key, value, time=900):
        return await self.redis_cache.execute_command("set", key, value, "ex", time)

    async def flush_db(self):
        await self.redis_cache.flushdb()

    async def close(self):
        await self.redis_cache.close()


redis_cache = RedisCache(os.environ.get("REDIS_CACHE_URL"))
