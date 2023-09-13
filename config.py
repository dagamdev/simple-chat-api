import environ

env = environ.Env()
environ.Env.read_env()

REDIS_URL = env('REDIS_URL')