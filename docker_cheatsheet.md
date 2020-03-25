# Cấu hình proxy cho docker
- Các cấu hình sau cho phép pull docker images từ internet qua proxy

- Thực hiện các lệnh sau dưới quyền root:

```sh
mkdir -p /etc/systemd/system/docker.service.d/
touch /etc/systemd/system/docker.service.d/{http-proxy.conf,https-proxy.conf}
cat << EOF > /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://192.168.5.8:3128/" "NO_PROXY=localhost,127.0.0.1,docker-registry"
EOF

cat << EOF > /etc/systemd/system/docker.service.d/https-proxy.conf
[Service]
Environment="HTTPS_PROXY=http://192.168.5.8:3128/" "NO_PROXY=localhost,127.0.0.1,docker-registry"
EOF
```

- Chú ý:
  - Sửa lại các các trị HTTP_PROXY và HTTPS_PROXY cho phù hợp với biến môi trường
  - Sửa lại giá trị ```docker-registry``` thành địa chỉ IP hoặc hostname của private docker registry nếu như muốn pull docker từ cả internet và private docker registry
  - Có thể bỏ giá trị docker-registry nếu không cần dùng private docker registry

- Restart docker:

```sh
systemctl daemon-reload
systemctl restart docker
```

# Build docker images qua proxy
Bước 2:
- Ví dụ có thư mục chứa docker như sau:

```sh
horizon __ Dockerfile
       |__ start.sh
       |__ copy.sh
       |__ ...
```
	   
- Build docker sau proxy sử dụng lệnh sau:

```sh
HTTP_PROXY=http://192.168.5.8:3128 
HTTPS_PROXY=http://192.168.5.8:3128 
docker build -t horizon:queens horizon --build-arg http_proxy=${HTTP_PROXY} --build-arg https_proxy=${HTTPS_PROXY}
```

- Chú ý:
  - Sửa lại hai giá trị HTTP_PROXY vaf HTTPS_PROXY cho phù hợp với môi trường
  - Cấu trúc lệnh build: ```docker build -t <image name>:<tag> <path to directory contains Dockerfile> --build-arg <key0>=<value0> <key1>=<value1>...```
  

# Sử dụng docker-compose sau proxy

- Ví dụ có thư mục chứa docker-compose file như sau:

```sh
sandbox __ docker-compose.yml
       |__ nginx-compose.yml
       |__ documentation
       |__ README.md
       |__ 
```

- Cấu trúc docker-compose dạng như sau:

```sh
version: '3.3'
services:
...
  documentation:
    build:
      context: ./documentation
    ports:
      - "3010:3000"
```

Chú ý sửa lại docker-compose version lớn hơn 2.2 để support option ```build-args``` khi build docker images từ docker-compose

- Pull và build các docker images trong docker-compose:

```sh
cd sandbox
HTTP_PROXY=http://192.168.5.8:3128 
HTTPS_PROXY=http://192.168.5.8:3128 
docker-compose build --build-arg http_proxy=${HTTP_PROXY} --build-arg https_proxy=${HTTPS_PROXY}
```

- Để build các images cho file docker-compose bất kì (mặc định file ```docker-compose.yml``` được sử dụng), sử dụng tùy chọn -f chỉ định file docker-compose. Ví dụ:

```sh
cd sandbox
HTTP_PROXY=http://192.168.5.8:3128 
HTTPS_PROXY=http://192.168.5.8:3128 
docker-compose build -f nginx-compose.yml --build-arg http_proxy=${HTTP_PROXY} --build-arg https_proxy=${HTTPS_PROXY}
```

- Các thao tác cơ bản với docker-compose:

  - Tạo stack các services từ docker-compose:
  
  ```sh
  docker-compose up -d
  ```
  
  - Hoặc chạy file docker-compose bất kì:
  
  ```sh
  docker-compose -f nginx-compose.yml up -d
  ```
  Sửa lại nginx-compose.yml thành tên file docker-compose phù hợp
  
  - Stop/start/restart tất cả các services trong stack
  
  ```sh
  docker-compose stop
  docker-compose start
  docker-compose restart
  ```
  
  - Hoặc stop/start/restart các services định nghĩa trong file compose bất kì:
  
  ```sh
  docker-compose -f nginx-compose.yml stop
  docker-compose -f nginx-compose.yml start
  docker-compose -f nginx-compose.yml restart
  ```
  
  - Xóa stack các services trong docker-compose:
  
  ```sh
  docker-compose stop
  docker-compose rm -f
  ```

  - Hoặc xóa stack các services trong file docker-compose bất kì:
  
  ```sh
  docker-compose -f nginx-compose.yml stop
  docker-compose -f nginx-compose.yml rm -f
  ```

Refs
---
1. https://github.com/wsargent/docker-cheat-sheet
