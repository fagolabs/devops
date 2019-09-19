FROM node:11-alpine

LABEL MAINTAINER="don@agilicus.com"
LABEL taiga_version="branch:master"

ENV TAIGA_VERSION master
ENV NODE_ENV production

WORKDIR /taiga_events
COPY scripts/ /scripts/
# Getting from branch master, they don't provide tags, or stable branch
# https://github.com/taigaio/taiga-events/issues/8

RUN apk add git \
    && git clone  https://github.com/donbowman/taiga-events  /taiga_events \
    && apk del git \
    && npm install --only=prod \
    && npm install --only=prod coffeescript \
    && addgroup -S taiga && adduser -S -G taiga taiga \
    && chown -R taiga /taiga_events \
    && chown -R taiga /scripts/ \
    && chmod +x /scripts/entrypoint.sh

USER taiga
ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["/taiga_events/node_modules/coffeescript/bin/coffee", "index.coffee"]
