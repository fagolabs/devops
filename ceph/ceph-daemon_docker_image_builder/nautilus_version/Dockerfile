# CEPH DAEMON IMAGE
# CEPH VERSION: Luminous
# CEPH VERSION DETAIL: 12.x.x

FROM ubuntu:16.04
MAINTAINER Sébastien Han "seb@redhat.com"

ENV CEPH_VERSION nautilus
ENV CONFD_VERSION 0.16.0
ENV KUBECTL_VERSION v1.8.11

# Install neccessary package
RUN apt-get update
RUN apt-get install -y ca-certificates
RUN apt-get install -y vim net-tools git python-pip

COPY forego-stable-linux-amd64.tgz /forego.tgz
COPY fake_authen_keystone.tar /fake_authen_keystone.tar
RUN tar xf /fake_authen_keystone.tar
RUN pip install -r /fake_authen_keystone/requirements.txt
RUN cd /fake_authen_keystone && git init && python setup.py install
RUN mkdir -p /opt/ceph-container/bin/

# Trust certificate
COPY equinox.io.crt.cer /equinox.io.crt.cer
#RUN mkdir /usr/local/share/ca-certificates
RUN cp /equinox.io.crt.cer /usr/local/share/ca-certificates/
RUN update-ca-certificates

# Packages list
ARG PACKAGES="ceph-mon ceph-osd ceph-mds ceph-mgr ceph-base ceph-common radosgw rbd-mirror sharutils etcd s3cmd nfs-ganesha nfs-ganesha-ceph nfs-ganesha-rgw lvm2"
ARG PURGES="/var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/lib/{dracut,locale,systemd,udev} /usr/bin/hyperkube /usr/bin/etcd /usr/bin/systemd-analyze /etc/{udev,selinux} /usr/lib/{udev,systemd}"
# Add s3cfg file
ADD ./ceph-container/src/daemon/s3cfg /root/.s3cfg

# Add bootstrap script, ceph defaults key/values for KV store
#ADD *.sh ceph.defaults check_zombie_mons.py ./osd_scenarios/* entrypoint.sh.in disabled_scenario /
#RUN cd ceph-container && git checkout -b lastest-version && cd ..
RUN mkdir -p /opt/ceph-container/bin
ADD ./ceph-container/src/daemon/*.sh /opt/ceph-container/bin/
ADD ./ceph-container/src/daemon/ceph.defaults /opt/ceph-container/bin/
ADD ./ceph-container/src/daemon/check_zombie_mons.py /opt/ceph-container/bin/
ADD ./ceph-container/src/daemon/osd_scenarios/* /opt/ceph-container/bin/
ADD ./ceph-container/src/daemon/entrypoint.sh.in /opt/ceph-container/bin/
ADD ./ceph-container/src/daemon/disabled_scenario /opt/ceph-container/bin/

# install prerequisites
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y wget unzip uuid-runtime python-setuptools udev dmsetup && \
  # Install ceph, ganesha and etcd
  wget -q -O- 'https://download.ceph.com/keys/release.asc' | apt-key add - && \
  echo "deb http://download.ceph.com/debian-$CEPH_VERSION/ xenial main" | tee /etc/apt/sources.list.d/ceph-$CEPH_VERSION.list && \
  echo "deb http://download.ceph.com/nfs-ganesha/deb-V2.5-stable/luminous/ xenial main" | tee /etc/apt/sources.list.d/nfs-ganesha.list && \
  apt-get update && apt-get install -y  --no-install-recommends --force-yes $PACKAGES && \
  dpkg -s $PACKAGES && \
  apt-get clean && rm -rf $PURGES && \
  # Download & install confd
  wget -O /usr/local/bin/confd "https://github.com/kelseyhightower/confd/releases/download/v${CONFD_VERSION}/confd-${CONFD_VERSION}-linux-amd64" && \
  chmod +x /usr/local/bin/confd && mkdir -p /etc/confd/conf.d && mkdir -p /etc/confd/templates && \
  # Install forego
  #wget -O /forego.tgz 'https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.tgz' && \
  cd /usr/local/bin && tar xfz /forego.tgz && chmod +x /usr/local/bin/forego && rm /forego.tgz && \
  # Install kubectl
  wget -O /usr/local/bin/kubectl "https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
  chmod +x /usr/local/bin/kubectl && \
  # Cleaning container
  #bash /clean_container.sh && rm /clean_container.sh
  echo hungdh9 bypass clean_container.sh

# Modify the entrypoint
RUN bash "/opt/ceph-container/bin/generate_entrypoint.sh" && \
  rm -f /opt/ceph-container/bin/generate_entrypoint.sh && \
  bash -n /opt/ceph-container/bin/*.sh

# Add templates for confd
ADD ./ceph-container/src/daemon/confd/templates/* /etc/confd/templates/
ADD ./ceph-container/src/daemon/confd/conf.d/* /etc/confd/conf.d/

# Add volumes for Ceph config and data
VOLUME ["/etc/ceph","/var/lib/ceph", "/etc/ganesha"]

# Execute the entrypoint
WORKDIR /
ENTRYPOINT ["/opt/ceph-container/bin/entrypoint.sh"]
LABEL head=d0e6104
