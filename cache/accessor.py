import redis


def get_redis_connection() -> redis.Redis:
    return redis.Redis(host="localhost", port=14000, db=0)
