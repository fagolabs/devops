FROM ubuntu:18.04 as builder
LABEL MAINTAINER="don@agilicus.com"
LABEL taiga_version="tag:4.1.0"

ENV TAIGA_VERSION 4.2.10
ENV DEBIAN_FRONTEND=noninteractive

ARG http_proxy
WORKDIR /taiga_backend
ADD https://github.com/taigaio/taiga-back/archive/${TAIGA_VERSION}.tar.gz ./

COPY scripts/ /scripts/

# https://github.com/psycopg/psycopg2-wheels/issues/2
# RUN sed -i 's?CairoSVG=?CairoSVG>?' requirements.txt
RUN apt-get update \
    && apt-get --yes install wget gnupg \
    && echo deb https://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main > /etc/apt/sources.list.d/pgdg.list \
    && wget -q -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get --yes --no-install-recommends install python3 build-essential libssl-dev \
       libfreetype6-dev libjpeg8-dev libwebp-dev libtiff5-dev libpng-dev liblcms2-2 \
       libopenjp2-7-dev zlib1g-dev libxslt1-dev libxml2-dev libffi-dev libpq-dev git \
       python3-pip postgresql-client-11 gettext curl python3-setuptools python3-wheel libpython3.6-dev \
    && tar -xzf ${TAIGA_VERSION}.tar.gz -C ./ taiga-back-${TAIGA_VERSION} --strip-components=1 \
    && rm ${TAIGA_VERSION}.tar.gz \
    && sed -i 's,git+https://github.com/Xof/django-pglocks.git,django-pglocks==1.0.2,g' requirements.txt \
    && echo "django-environ==0.4.0" >> requirements.txt \
    && echo "gevent>=1.4.0" >> requirements.txt \
    && echo "django-anymail==0.5" >> requirements.txt \
    && echo "taiga-contrib-gitlab-auth-official>=3.1.1" >> requirements.txt \
    && echo "django-dbbackup" >> requirements.txt \
    && echo "django-cron" >> requirements.txt \
    && sed -i -e 's?gunicorn==19.7.1?gunicorn==19.9.0?g' requirements.txt \
    && sed -i -e 's?celery==4.0.2?celery==4.2.1?g' requirements.txt \
    && sed -i -e 's?kombu==4.0.2?kombu>=4.2.1?g' requirements.txt \
    && pip3 --proxy=$http_proxy install -r requirements.txt \
    && python3 manage.py compilemessages \
    && git clone https://github.com/donbowman/taiga-contrib-google-auth.git \
    && cd taiga-contrib-google-auth/back \
    && pip3 install . \
    && pip3 install gnupg \
    && pip3 install django-extensions \
    && mkdir -p /taiga_backend/media /taiga_backend/static-root \
    && adduser --disabled-password --gecos '' taiga  \
    && chown taiga:taiga /var/backups \
    && chown -R taiga:taiga /usr/local/lib/python3.6/dist-packages/taiga_contrib* \
    && chown -R taiga:taiga /taiga_backend \
    && chown -R taiga:taiga /scripts/ \
    && chmod 555 /scripts/entrypoint.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache

COPY local.py settings/local.py
COPY celery_local.py settings/celery_local.py

USER taiga
