FROM ubuntu:18.04
MAINTAINER thaihust

WORKDIR /opt

COPY files/suricata-4.1.4.tar.gz /opt

RUN apt-get update \
    && apt-get upgrade --yes \
    && apt-get --yes install libpcre3 libpcre3-dbg libpcre3-dev \
       build-essential autoconf automake libtool libpcap-dev libnet1-dev \
       libyaml-0-2 libyaml-dev zlib1g zlib1g-dev make flex bison libmagic-dev \
       libjansson-dev libjansson4 libnss3-dev libnspr4-dev libgeoip1 libgeoip-dev \
       libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev \
       libnfnetlink0  libcap-ng0 libcap-ng-dev oinkmaster ethtool curl cron \
       python-simplejson libluajit-5.1-dev luajit ulogd2 psmisc pkg-config

RUN apt-get -y install libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev libnfnetlink0

RUN apt-get -y install python-pip

RUN pip install --upgrade suricata-update && ln -s /usr/local/bin/suricata-update /usr/bin/suricata-update

RUN tar xfvz /opt/suricata-4.1.4.tar.gz \
    && cd suricata-4.1.4 \
    && ./configure --prefix=/usr/ --sysconfdir=/etc/ --localstatedir=/var/ \
    --disable-gccmarch-native --with-libnss-libraries=/usr/lib \
    --with-libnss-includes=/usr/include/nss/ --enable-nfqueue \
    --with-libcap_ng-libraries=/usr/local/lib --with-libcap_ng-includes=/usr/local/include \
    --with-libnspr-libraries=/usr/lib \
    --with-libnspr-includes=/usr/include/nspr \
    --with-nflog \
    --with-libluajit \
    && make clean \
    && make \
    && make install-full \
    && ldconfig \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm -rf /opt/suricata-4.1.4 /opt/suricata-4.1.4.tar.gz

VOLUME /etc/suricata
VOLUME /etc/suricata/rules
VOLUME /var/log/suricata

ADD files/oinkmaster.conf /etc/oinkmaster.conf
ADD files/blacklist.sh /blacklists.sh
ADD files/start.sh /start.sh
RUN chmod u+x /start.sh /blacklists.sh
ENTRYPOINT ["/start.sh"]
