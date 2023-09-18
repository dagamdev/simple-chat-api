import environ

env = environ.Env()
environ.Env.read_env()

class EnvVariables():
  ENGINE = env('ENGINE')
  NAME = env('NAME')
  USER = env('USER')
  PASSWORD = env('PASSWORD')
  HOST = env('HOST')
  PORT = env('PORT')

  REDIS_URL = env('REDIS_URL')
  IN_DEVELOPMENT = env('IN_DEVELOPMENT')
