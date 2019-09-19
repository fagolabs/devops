#!/bin/sh
set -e

if [ ! -f /taiga_events/config.json ]; then
    echo "Generating /taiga_events/config.json file..."
    cat > /taiga_events/config.json <<EOF
{
    "url": "amqp://${RABBITMQ_DEFAULT_USER}:${RABBITMQ_DEFAULT_PASS}@${TAIGA_RABBITMQ}:5672/${RABBITMQ_DEFAULT_VHOST}",
    "secret": "$TAIGA_SECRET",
    "webSocketServer": {
        "port": 8888
    }
}

EOF
fi

exec "$@"
