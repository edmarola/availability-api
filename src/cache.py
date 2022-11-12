import os

import redis

r = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])
