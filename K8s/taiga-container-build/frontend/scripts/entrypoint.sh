#!/bin/sh

set -o errexit

if [ ! -f /taiga_frontend/conf.json ]; then
    echo "Generating /taiga_frontend/conf.json file..."
    TAIGA_API_URL=${TAIGA_API_URL:-/api/v1/}
    DEFAULT_LANGUAGE=${DEFAULT_LANGUAGE:-en}
    TAIGA_EVENTS_URL=${TAIGA_EVENTS_URL:-null}
env
    cat > /taiga_frontend/conf.json <<EOF
{
    "api": "$TAIGA_API_URL",
    "eventsUrl": "$TAIGA_EVENTS_URL",
    "eventsMaxMissedHeartbeats": 5,
    "eventsHeartbeatIntervalTime": 60000,
    "debug": ${TAIGA_DEBUG:-false},
    "debugInfo": ${TAIGA_DEBUG:-false},
    "defaultLanguage": "$DEFAULT_LANGUAGE",
    "themes": ["taiga"],
    "defaultTheme": "taiga",
    "publicRegisterEnabled": ${TAIGA_PUBLIC_REGISTER_ENABLED:-true},
    "feedbackEnabled": true,
    "privacyPolicyUrl": null,
    "termsOfServiceUrl": null,
    "maxUploadFileSize": null,
    "gitLabUrl": "${GITLAB_URL:-null}",
    "gitLabClientId": "${GITLAB_API_CLIENT_ID:-null}",
    "googleClientId": "${GOOGLE_API_CLIENT_ID:-null}",
    "contribPlugins": [
EOF
    [ -n "$GITLAB_API_CLIENT_ID" ] && echo \"/plugins/google-auth/gitlab-auth.json\" >> /taiga_frontend/conf.json
    [ -n "$GITLAB_API_CLIENT_ID" -a -n "$GOOGLE_API_CLIENT_ID" ] && echo , >> /taiga_frontend/conf.json
    [ -n "$GOOGLE_API_CLIENT_ID" ] && echo \"/plugins/google-auth/google-auth.json\" >> /taiga_frontend/conf.json


cat >> /taiga_frontend/conf.json << EOF1
]
}
EOF1
fi

TAIGA_BACKEND="${TAIGA_BACKEND:-backend}"
TAIGA_EVENTS="${TAIGA_EVENTS:-events}"

sed -e "s?TAIGA_BACKEND?$TAIGA_BACKEND?g" -e "s?TAIGA_EVENTS?$TAIGA_EVENTS?g" /etc/nginx/nginx.conf.tmpl > /etc/nginx/nginx.conf
sed -e "s?TAIGA_BACKEND?$TAIGA_BACKEND?g" -e "s?TAIGA_EVENTS?$TAIGA_EVENTS?g"  /etc/nginx/conf.d/default.conf.tmpl> /etc/nginx/conf.d/default.conf

exec "$@"
