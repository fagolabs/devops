# 1. Setup docker & docker-compose
```sh
apt-get update
bash setup_docker.sh
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

# 2. Setup python 
```sh
apt-get install -y python python-pip
pip install requests
```

# 3. System config for elasticsearch
```sh
echo vm.max_map_count=262144 >> /etc/sysctl.conf
```

# 4. Setup ELK 
```sh
docker-compose up -d
```

# 5. Access Kibana
- Kibana portal: http://127.0.0.1:5601
