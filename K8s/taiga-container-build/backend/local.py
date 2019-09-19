# -*- coding: utf-8 -*-
# https://github.com/taigaio/taiga-back/blob/master/settings/local.py.example
from .common import *
import environ


env = environ.Env()
DEBUG = env('DJANGO_DEBUG', cast=bool, default=False)
PUBLIC_REGISTER_ENABLED = env(
    'TAIGA_PUBLIC_REGISTER_ENABLED', cast=bool, default=True
)

SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', cast=list, default=['*'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DJANGO_DB_NAME'),
        'USER': env('DJANGO_DB_USER'),
        'PASSWORD': env('DJANGO_DB_PASSWORD'),
        'HOST': env('TAIGA_POSTGRESQL'),
        'PORT': '',
    }
}

TAIGA_HOSTNAME = env('TAIGA_HOSTNAME', default='localhost')

_HTTP = 'https' if env('TAIGA_SSL', cast=bool, default=False) else 'http'

SITES = {
    "api": {
       "scheme": _HTTP,
       "domain": TAIGA_HOSTNAME,
       "name": "api"
    },
    "front": {
      "scheme": _HTTP,
      "domain": TAIGA_HOSTNAME,
      "name": "front"
    },
}

SITE_ID = "api"

MEDIA_URL = "{}://{}/media/".format(_HTTP, TAIGA_HOSTNAME)
STATIC_URL = "{}://{}/static/".format(_HTTP, TAIGA_HOSTNAME)
MEDIA_ROOT = '/taiga_backend/media'
STATIC_ROOT = '/taiga_backend/static-root'

# Async
# see celery_local.py
# BROKER_URL = 'amqp://taiga:taiga@rabbitmq:5672/taiga'
EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
EVENTS_PUSH_BACKEND_OPTIONS = {"url": "amqp://%s:%s@%s:5672/%s" % (env("RABBITMQ_DEFAULT_USER"), env("RABBITMQ_DEFAULT_PASS"), env("TAIGA_RABBITMQ"), env("RABBITMQ_DEFAULT_VHOST") ) }

# see celery_local.py
CELERY_ENABLED = True

if len(env('EMAIL_HOST', cast=str, default = '')):
    EMAIL_HOST = env('EMAIL_HOST', cast=str, default = '')
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', cast=str, default='anonymous@example.com')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', cast=str, default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', cast=str, default='')
    EMAIL_PORT = env('EMAIL_PORT', cast=int, default=587)
    EMAIL_SUBJECT_PREFIX='[taiga] '

INSTALLED_APPS += ["django_extensions"]

if len(env('TAIGA_BACKUP_DIR', cast=str, default='')):
    print("Enable backup")
    INSTALLED_APPS += ["dbbackup"]
    INSTALLED_APPS += ["django_cron"]
    DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
    DBBACKUP_STORAGE_OPTIONS = {'location': env('TAIGA_BACKUP_DIR', cast=str, default='') }
#
#    import os
#    import ast
#    from django.core import management
#    from django.conf import settings
#    from django_cron import CronJobBase, Schedule
#
#    class Backup(CronJobBase):
#        RUN_AT_TIMES = ast.literal_eval(env('TAIGA_BACKUP_TIMES', cast=str, default="['22:45']"))
#        print("RUN_AT_TIMES: <<%s>>" % RUN_AT_TIMES)
#        schedule = Schedule(run_at_times=RUN_AT_TIMES)
#        code = 'taiga.Backup'
#
#        def do(self):
#            print("\n************** Do backup ***********************\n")
#            management.call_command('dbbackup', '-z')
#            management.call_command('mediabackup', '-z')
#    CRON_CLASSES = [
#        "taiga.Backup"
#    ]

if len(env('GOOGLE_API_CLIENT_ID', cast=str, default='')):
        INSTALLED_APPS += ["taiga_contrib_google_auth"]

        # Get these from https://console.cloud.google.com/apis/credentials
        GOOGLE_API_CLIENT_ID = env("GOOGLE_API_CLIENT_ID")
        GOOGLE_API_CLIENT_SECRET = env("GOOGLE_API_CLIENT_SECRET")
        GOOGLE_API_REDIRECT_URI = env("GOOGLE_API_REDIRECT_URI")
        GOOGLE_RESTRICT_LOGIN = [env("GOOGLE_RESTRICT_LOGIN")]
        GOOGLE_API_ALLOW_DOMAIN = [env("GOOGLE_API_ALLOW_DOMAIN")]

if len(env('GITLAB_API_CLIENT_ID', cast=str, default='')):
        INSTALLED_APPS += ["taiga_contrib_gitlab_auth"]

        # Get these from Admin -> Applications
        GITLAB_API_CLIENT_ID = env("GITLAB_API_CLIENT_ID")
        GITLAB_API_CLIENT_SECRET = env("GITLAB_API_CLIENT_SECRET")
        GITLAB_URL = env("GITLAB_URL")

# Mail settings
if env('USE_ANYMAIL', cast=bool, default=False):
    INSTALLED_APPS += ['anymail']
    ANYMAIL = {
        "MAILGUN_API_KEY": env('ANYMAIL_MAILGUN_API_KEY'),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
    DEFAULT_FROM_EMAIL = "Taiga <{}>".format(env('DJANGO_DEFAULT_FROM_EMAIL'))

# Cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "unique-snowflake"
#     }
# }

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}

if (DEBUG):
    LOGGING['handlers']['console']['level'] = 'DEBUG'
    LOGGING['loggers']['django']['level'] = 'DEBUG'

import logging, logging.config
logging.config.dictConfig(LOGGING)
