### Build:

```
docker build -t <image_name>:<image_tag> [--build-arg http_proxy=<http_proxy_addr>] [--build-arg https_proxy=<https_proxy_addr>] .
docker push <image_name>:<image_tag>
```

### Save image
```
docker save <image_name>:<image_tag> -o <file_name>.tar
```

### Load image
```
docker load -i <file_name>.tar
```

### Run docker image ceph-daemon
Docker image Ceph-daemon used to be run daemon element instances of Ceph cluster such as mon, mgr, osd, rgw, mds,...

You can find guilde to run each of that daemon element instances here: https://hub.docker.com/r/ceph/daemon/
