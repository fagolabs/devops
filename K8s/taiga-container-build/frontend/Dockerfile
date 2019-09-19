FROM ubuntu:18.04

LABEL maintainer="don@agilicus.com"
LABEL taiga_version="tag:4.1.1"

ENV TAIGA_VERSION 4.2.1
ENV DEBIAN_FRONTEND=noninteractive
ARG http_proxy

# Entrypoint
COPY scripts/ /scripts/
# Frontend compiled code
ADD https://github.com/taigaio/taiga-front-dist/archive/${TAIGA_VERSION}-stable.tar.gz /taiga_frontend/
WORKDIR /taiga_frontend

RUN apt-get update \
    && apt-get install -y nginx wget curl \
    && tar -xzf ${TAIGA_VERSION}-stable.tar.gz -C ./ taiga-front-dist-${TAIGA_VERSION}-stable/ --strip-components=2 \
    && rm ${TAIGA_VERSION}-stable.tar.gz \
    && addgroup --gid 1000 taiga \
    && adduser --uid 1000 --gid 1000 --gecos "" --disabled-login taiga \
    && chmod 555 /scripts/entrypoint.sh \
    && rm -f /etc/nginx/sites-enabled/default \
    && mkdir -p /taiga_frontend/plugins/google-auth/images /taiga_frontend/plugins/gitlab-auth/images \
    && wget -O /taiga_frontend/plugins/google-auth/google-auth.js https://raw.githubusercontent.com/donbowman/taiga-contrib-google-auth/master/front/dist/google-auth.js \
    && wget -O /taiga_frontend/plugins/google-auth/google-auth.json https://raw.githubusercontent.com/donbowman/taiga-contrib-google-auth/master/front/dist/google-auth.json \
    && wget -O /taiga_frontend/plugins/google-auth/images/google-logo.png https://raw.githubusercontent.com/donbowman/taiga-contrib-google-auth/master/front/images/google-logo.png \
    && wget -O /taiga_frontend/plugins/gitlab-auth/gitlab-auth.js https://raw.githubusercontent.com/taigaio/taiga-contrib-gitlab-auth/master/front/dist/gitlab-auth.js \
    && wget -O /taiga_frontend/plugins/gitlab-auth/gitlab-auth.json https://raw.githubusercontent.com/taigaio/taiga-contrib-gitlab-auth/master/front/dist/gitlab-auth.json \
    && wget -O /taiga_frontend/plugins/gitlab-auth/images/gitlab-logo.png https://github.com/taigaio/taiga-contrib-gitlab-auth/raw/master/front/dist/images/gitlab-logo.png \
    && touch /run/nginx.pid \
    && chown -R taiga:taiga /taiga_frontend /scripts /etc/nginx /var/lib/nginx /var/log/nginx /run/nginx.pid \
    && chown -R taiga:taiga /scripts/

COPY nginx/default.conf.tmpl /etc/nginx/conf.d/default.conf.tmpl
COPY nginx/nginx.conf.tmpl /etc/nginx/nginx.conf.tmpl

USER taiga
ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
