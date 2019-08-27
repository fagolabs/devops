import os

ALLOWED_HOSTS = ['*']

USE_ELASTICSEARCH = True
ELASTICSEARCH_ADDRESS = "127.0.0.1:9200"
ELASTICSEARCH_VERSION = 6
#ELASTICSEARCH_2X = True
KIBANA_VERSION = 6
KIBANA_INDEX = ".kibana"
KIBANA_URL = "http://127.0.0.1:5601"
KIBANA6_DASHBOARDS_PATH = "/opt/kibana-dashboards"

SURICATA_UNIX_SOCKET = "/var/run/suricata/suricata-command.socket"

USE_KIBANA = True
KIBANA_PROXY = True
KIBANA_DASHBOARDS_COUNT = 25

USE_EVEBOX = True
EVEBOX_ADDRESS = "127.0.0.1:5636"

USE_SURICATA_STATS = True
USE_LOGSTASH_STATS = True
ELASTICSEARCH_LOGSTASH_ALERT_INDEX="logstash-alert-"

USE_MOLOCH = True
MOLOCH_URL = "http://localhost:8005"

DATA_DIR = "/sciriusdata/"
STATIC_ROOT = "/sciriusstatic/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'scirius.sqlite3'),
    }
}

GIT_SOURCES_BASE_DIRECTORY = os.path.join(DATA_DIR, 'git-sources/')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backups/'}
