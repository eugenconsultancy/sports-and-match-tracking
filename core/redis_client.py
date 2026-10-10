"""
Redis client utility for caching and pub/sub.
"""
import json
import redis
from django.conf import settings
from functools import wraps
import hashlib
import pickle


class RedisClient:
    """Redis client wrapper for the application."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        redis_url = settings.CACHES['default']['LOCATION']
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.client.pubsub()
        self._initialized = True
    
    def get(self, key):
        """Get value from cache."""
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key, value, timeout=300):
        """Set value in cache with TTL."""
        serialized = json.dumps(value)
        return self.client.setex(key, timeout, serialized)
    
    def delete(self, key):
        """Delete key from cache."""
        return self.client.delete(key)
    
    def get_or_set(self, key, callback, timeout=300):
        """Get from cache or compute and store."""
        value = self.get(key)
        if value is not None:
            return value
        
        value = callback()
        self.set(key, value, timeout)
        return value
    
    def invalidate_pattern(self, pattern):
        """Invalidate all keys matching pattern."""
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0
    
    def publish(self, channel, message):
        """Publish message to a channel."""
        serialized = json.dumps(message)
        return self.client.publish(channel, serialized)
    
    def subscribe(self, channel):
        """Subscribe to a channel."""
        self.pubsub.subscribe(channel)
    
    def listen(self):
        """Listen for messages on subscribed channels."""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                yield {
                    'channel': message['channel'],
                    'data': json.loads(message['data'])
                }
    
    def cache_key(self, *args, **kwargs):
        """Generate a cache key from arguments."""
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key_string = ':'.join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def lock(self, lock_key, timeout=30):
        """Acquire a distributed lock."""
        return self.client.lock(
            f"lock:{lock_key}",
            timeout=timeout,
            blocking_timeout=5
        )


# Singleton instance
redis_client = RedisClient()


def cache_result(timeout=300, prefix=''):
    """
    Decorator to cache function results in Redis.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key_parts = [prefix, func.__module__, func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = ':'.join(key_parts)
            
            # Try cache
            cached = redis_client.get(cache_key)
            if cached is not None:
                return cached
            
            # Compute and cache
            result = func(*args, **kwargs)
            redis_client.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator