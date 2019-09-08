### Build:

```
docker build -t docker-registry:4000/ceph-daemon:mimic-selfbuild --build-arg http_proxy=http://192.168.5.8:3128 --build-arg https_proxy=http://192.168.5.8:3128 .
docker push docker-registry:4000/ceph-daemon:mimic-selfbuild
```

### Start

```
docker run -tid --name openstack-client --network=host -v /usr/share/docker/:/usr/share/docker/ -v /etc/localtime:/etc/localtime -u root -e SHARED_CONF_DIR='/usr/share/docker' docker-registry:4000/openstack-client:<tag>
