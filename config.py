import environ

env = environ.Env()
environ.Env.read_env()

class EnvVariables():
  DJANGO_SECRET_KEY = env('DJANGO_SECRET_KEY')
  
  ENGINE = env('ENGINE')
  NAME = env('NAME')
  USER = env('USER')
  PASSWORD = env('PASSWORD')
  HOST = env('HOST')
  POSTGRESQL_PORT = env('POSTGRESQL_PORT')

  REDIS_URL = env('REDIS_URL')
  IN_DEVELOPMENT = env('IN_DEVELOPMENT')
