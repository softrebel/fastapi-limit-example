import redis,os
redis_client = redis.Redis(host=os.getenv('REDIS_HOST'))
def limiter(key, limit):
    req = redis_client.incr(key)
    ttl=60
    if req == 1:
        redis_client.expire(key, ttl)
    else:
        ttl = redis_client.ttl(key)
    if req > limit:
        return {
            "call": False,
            "ttl": ttl
        }
    else:
        return {
            "call": True,
            "ttl": ttl
        }



def call_limiter(ip, limit):
    key=f'call_{ip}'
    return limiter(key, limit)

def bad_call_limiter(ip, limit):
    key=f'bad_call_{ip}'
    return limiter(key, limit)
