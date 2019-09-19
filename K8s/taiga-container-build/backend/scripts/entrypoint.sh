#!/bin/sh

RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER:-taiga}
RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS:-taiga}
RABBITMQ_DEFAULT_VHOST=${RABBITMQ_DEFAULT_VHOST:-taiga}
TAIGA_RABBITMQ=${TAIGA_RABBITMQ:-rabbitmq}
TAIGA_REDIS=${TAIGA_REDIS:-redis}
TAIGA_POSTGRESQL=${TAIGA_POSTGRESQL:-postgresql}

env

echo "Check for postgres to be up @ ${TAIGA_POSTGRESQL}:5432"
until timeout 1 bash -c "cat < /dev/null > /dev/tcp/$TAIGA_POSTGRESQL/5432"
do
    echo "Wait for postgresql..."
    sleep 1
done

# Block for database to be ready and then set it up

# Setup database automatically if needed
if [ -z "$TAIGA_SKIP_DB_CHECK" ]; then
  DB_CHECK_STATUS=$(python3 /scripts/checkdb.py)
  if [ "$DB_CHECK_STATUS" = "missing_django_migrations" ]; then
    echo "Configuring initial database"
    sleep 2
    echo "migrate --noinput"
    until timeout 30 python3 /taiga_backend/manage.py migrate --noinput; do sleep 1; done
    echo "loaddata initial_user"
    until timeout 30 python3 /taiga_backend/manage.py loaddata -v2 initial_user; do sleep 1; done
    echo "loaddata initial_project_templates"
    until timeout 30 python3 /taiga_backend/manage.py loaddata -v2 initial_project_templates; do sleep 1; done
  fi
fi

set -e

# Look for static folder, if it does not exist, then generate it
if [ ! -d /taiga_backend/static-root/admin ]; then
  echo "Collect static"
  python3 /taiga_backend/manage.py collectstatic --noinput
fi

pmc() {
    TAIGA_BACKUP_TIME=${TAIGA_BACKUP_TIME:-23:10}
    if [ ! -z "$TAIGA_BACKUP_DIR" ]
    then
        while true
        do
            now=$(date +%s)
            target=$(date -d $TAIGA_BACKUP_TIME +%s)
            ts=$((target - now))
            ots=$ts
            if [ $ts -lt 0 ]
            then
                ts=1
            fi
            echo "Sleep $ts seconds before next backup"
            sleep $ts
            python3 manage.py dbbackup -z
            python3 manage.py mediabackup -z
            PGPASSWORD=$POSTGRES_PASSWORD pg_dump --host taiga-postgresql -U taiga -Fc > $TAIGA_BACKUP_DIR/db-$(date -Is).pgdump

            # Now sleep less than 1 day and let above catch it up
            nd=86000
            if [ $ots -lt 0 ]
            then
                nd=$((nd + ots))
            fi
            echo "sleep $nd seconds until tomorrow"
            sleep $nd
        done
    fi
}

#pmc &
echo "Start $@"
exec "$@"
