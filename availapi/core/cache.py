import os

import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])
