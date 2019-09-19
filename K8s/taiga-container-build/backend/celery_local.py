from .celery import *
import environ

env = environ.Env()

broker_url = "amqp://%s:%s@%s:5672/%s" % (env("RABBITMQ_DEFAULT_USER"), env("RABBITMQ_DEFAULT_PASS"), env("TAIGA_RABBITMQ"), env("RABBITMQ_DEFAULT_VHOST"))

result_backend = "redis://%s:6379/0" % env("TAIGA_REDIS")
