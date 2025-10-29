from redis import asyncio as aioredis
from typing import Optional
import json

from core.logger import logger


class RedisManager:
    """Redis connection manager"""
    
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self._url: Optional[str] = None
    
    async def connect(self, url: str = None):
        """Connect to Redis"""
        from core.config import settings
        
        self._url = url or settings.REDIS_URL
        
        try:
            self.redis = await aioredis.from_url(
                self._url,
                encoding="utf-8",
                decode_responses=settings.REDIS_DECODE_RESPONSES
            )
            # Test connection
            await self.redis.ping()
            logger.info(f"✅ Redis connected: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis = None
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
            logger.info("👋 Redis disconnected")
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        if not self.redis:
            return None
        
        try:
            value = await self.redis.get(key)
            if value:
                logger.debug(f"✅ Cache HIT: {key}")
            else:
                logger.debug(f"❌ Cache MISS: {key}")
            return value
        except Exception as e:
            logger.error(f"❌ Redis GET error: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: str, 
        ttl: int = 300
    ) -> bool:
        """Set value in Redis with TTL"""
        if not self.redis:
            return False
        
        try:
            await self.redis.setex(key, ttl, value)
            logger.debug(f"✅ Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"❌ Redis SET error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.redis:
            return False
        
        try:
            await self.redis.delete(key)
            logger.debug(f"🗑️  Cache DELETE: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ Redis DELETE error: {e}")
            return False
    
    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value from Redis"""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON in cache: {key}")
                return None
        return None
    
    async def set_json(
        self, 
        key: str, 
        value: dict, 
        ttl: int = 300
    ) -> bool:
        """Set JSON value in Redis"""
        try:
            json_str = json.dumps(value)
            return await self.set(key, json_str, ttl)
        except Exception as e:
            logger.error(f"❌ JSON serialization error: {e}")
            return False
    
    async def get_ttl(self, key: str) -> int:
        """Get remaining TTL for key"""
        if not self.redis:
            return -1
        
        try:
            return await self.redis.ttl(key)
        except Exception as e:
            logger.error(f"❌ Redis TTL error: {e}")
            return -1
    
    async def keys(self, pattern: str = "*") -> list:
        """Get all keys matching pattern"""
        if not self.redis:
            return []
        
        try:
            return await self.redis.keys(pattern)
        except Exception as e:
            logger.error(f"❌ Redis KEYS error: {e}")
            return []


# Global Redis manager instance
redis_manager = RedisManager()
