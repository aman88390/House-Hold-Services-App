
from flask_caching import Cache
cache_config = {
    "CACHE_TYPE": "RedisCache",  
    "CACHE_REDIS_URL": "redis://localhost:6379/0"  
}

cache = Cache(config=cache_config)
