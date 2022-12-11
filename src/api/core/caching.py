import json
import os
import redis
from typing import Any, Callable, Dict, Optional
from dotenv import load_dotenv

from api.core.api_config import CACHE_EXPIRE

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASS = os.environ.get("REDIS_PASS")
REDIS_USER = os.environ.get("REDIS_USER")


def get_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASS,
        db=0,
        username=REDIS_USER,
    )


def author_fkey_formatter(author_id: int) -> str:
    return "author_{aid}".format(aid=author_id)


def cache_response(
    uniq_id: int,
    fkey_formatter: Callable[[int], str],
    key: str,
    dct_data: Dict[str, Any],
    expire: int = CACHE_EXPIRE,
) -> None:
    client = get_client()
    fkey = fkey_formatter(uniq_id)
    json_data = json.dumps(dct_data)
    client.hset(name=fkey, key=key, value=json_data)
    client.expire(fkey, expire)


def get_from_cache(
    uniq_id: int,
    fkey_formatter: Callable[[int], str],
    key: str,
) -> Optional[Dict[str, Any]]:
    client = get_client()
    fkey = fkey_formatter(uniq_id)
    json_data: Optional[bytes] = client.hget(name=fkey, key=key)

    if json_data is None:
        return None

    return json.loads(json_data.decode("utf-8"))


def cache(
    formatter: Callable[[int], str],
    id_arg_name: str,
    key: str,
    expire: int = CACHE_EXPIRE,
) -> Callable[[Callable], Callable]:
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            uniq_id = kwargs.get(id_arg_name)
            cached_val = None
            if uniq_id:
                cached_val = get_from_cache(uniq_id, formatter, key)

            if cached_val is not None:
                return cached_val

            uncached_val = func(*args, **kwargs)
            if uniq_id:
                cache_response(uniq_id, formatter, key, uncached_val, expire)

            return uncached_val

        return wrapper

    return decorator
