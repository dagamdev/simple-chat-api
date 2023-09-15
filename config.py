import environ

env = environ.Env()
environ.Env.read_env()

REDIS_URL = env('REDIS_URL')
IN_DEVELOPMENT = env('IN_DEVELOPMENT')