## Build Suricata IDS images

```
docker build -t thaihust/suricata:4.1.4 .
```

## Example usage

```
mkdir -p /usr/src/suricata/{configs,logs}
cp -r ./configs/. /usr/src/suricata/configs
docker run --name=suricata --net=host --privileged=true \
  -e DEVICE=eth0 \
  -v /usr/src/suricata/configs:/etc/suricata \
  -v /usr/src/suricata/logs:/var/log/suricata \
-d thaihust/suricata:4.1.4
```

## Notes: The container can take the following commands:
 * update - Runs oinkmaster.
 * build-info - Outputs the build information for Suricata.
 * shell - Bash shell
