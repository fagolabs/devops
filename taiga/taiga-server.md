# Cài đặt Taiga

Hướng dẫn cài đặt Taiga trên server

1. [Giới thiệu kiến trúc](#1-giới-thiệu)
2. [Cài đặt](#2-cài-đặt)
3. [Script cài đặt](#3-Script-cài-đặt)

## 1. Giới thiệu

Taiga gồm hai thành phần chính là: taiga-back và taiga-frontend 
- taiga-back: xây dựng trên Django, Python3 và expose API endpoint
- taiga-frontend: dùng Angularjs và coffeescript

## 2. Cài đặt

Môi trường cài đặt là ubuntu 18.04

### 2.1 Setup môi trường

Cài đặt các gói yêu cầu:

```bash
sudo apt-get update
sudo apt-get install -y build-essential binutils-doc autoconf flex bison libjpeg-dev
sudo apt-get install -y libfreetype6-dev zlib1g-dev libzmq3-dev libgdbm-dev libncurses5-dev
sudo apt-get install -y automake libtool curl git tmux gettext
sudo apt-get install -y nginx
sudo apt-get install -y rabbitmq-server redis-server
```

Cài Postgresql:

```bash
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt -y install postgresql-10
```

Cài Python và virtualenvwrapper

```bash
sudo apt-get install -y python3 python3-pip python3-dev virtualenvwrapper
sudo apt-get install -y libxml2-dev libxslt-dev
sudo apt-get install -y libssl-dev libffi-dev
```

Thêm user taiga

```bash
sudo adduser taiga
sudo adduser taiga sudo
sudo su taiga
cd ~
```

Cấu hình database:

```bash
sudo -u postgres createuser taiga
sudo -u postgres createdb taiga -O taiga --encoding='utf-8' --locale=en_US.utf8 --template=template0
```

### 2.2 Cấu hình backend

Download code

```bash
cd ~
git clone https://github.com/taigaio/taiga-back.git taiga-back
cd taiga-back
git checkout stable
```

Tạo virtualenv:

```bash
mkvirtualenv -p /usr/bin/python3 taiga
```

Cài các thành phần phụ thuộc:

```bash
pip install -r requirements.txt
```

Thêm dữ liệu khởi tạo trên database

```bash
python manage.py migrate --noinput
python manage.py loaddata initial_user
python manage.py loaddata initial_project_templates
python manage.py compilemessages
python manage.py collectstatic --noinput
```

Tạo file cấu hình `~/taiga-back/settings/local.py` và sửa các trường theo ý muốn

```python
from .common import *

MEDIA_URL = "http://example.com/media/"
STATIC_URL = "http://example.com/static/"
SITES["front"]["scheme"] = "http"
SITES["front"]["domain"] = "example.com"

SECRET_KEY = "theveryultratopsecretkey"

DEBUG = False
PUBLIC_REGISTER_ENABLED = True

DEFAULT_FROM_EMAIL = "no-reply@example.com"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

#CELERY_ENABLED = True

EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
EVENTS_PUSH_BACKEND_OPTIONS = {"url": "amqp://taiga:PASSWORD_FOR_EVENTS@localhost:5672/taiga"}

# Uncomment and populate with proper connection parameters
# for enable email sending. EMAIL_HOST_USER should end by @domain.tld
#EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#EMAIL_USE_TLS = False
#EMAIL_HOST = "localhost"
#EMAIL_HOST_USER = ""
#EMAIL_HOST_PASSWORD = ""
#EMAIL_PORT = 25

# Uncomment and populate with proper connection parameters
# for enable github login/singin.
#GITHUB_API_CLIENT_ID = "yourgithubclientid"
#GITHUB_API_CLIENT_SECRET = "yourgithubclientsecret"
```

Có thể kiểm tra xem các cài đặt cho backends đã đúng chưa:

```bash
workon taiga
python manage.py runserver
```

Sau đó truy nhập vào đường dẫn sau:

```bash
curl http://localhost:8000/api/v1/
```

nếu kết quả trả về là json thì ok.

### 2.3 Cấu hình Frontend

Download code:

```bash
cd ~
git clone https://github.com/taigaio/taiga-front-dist.git taiga-front-dist
cd taiga-front-dist
git checkout stable
```

Copy file cấu hình và sửa nó theo ý muốn:

```bash
cp ~/taiga-front-dist/dist/conf.example.json ~/taiga-front-dist/dist/conf.json
```

### 2.4 Khởi chạy dịch vụ

Chạy backend với gunicorn và tạo service systemd cho nó:

```bash
cat > /etc/systemd/system/taiga.serivce << EOF
[Unit]
Description=taiga_back
After=network.target

[Service]
User=taiga
Environment=PYTHONUNBUFFERED=true
WorkingDirectory=/home/taiga/taiga-back
ExecStart=/home/taiga/.virtualenvs/taiga/bin/gunicorn --workers 4 --timeout 60 -b 127.0.0.1:8001 taiga.wsgi
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF
sudo systemctl daemon-reload
sudo systemctl start taiga
sudo systemctl enable taiga
```

Chạy Nginx:

```bash
sudo rm /etc/nginx/sites-enabled/default
mkdir -p ~/logs

cat > /etc/nginx/conf.d/taiga.conf << EOF
server {
    listen 80 default_server;
    server_name _;

    large_client_header_buffers 4 32k;
    client_max_body_size 50M;
    charset utf-8;

    access_log /home/taiga/logs/nginx.access.log;
    error_log /home/taiga/logs/nginx.error.log;

    # Frontend
    location / {
        root /home/taiga/taiga-front-dist/dist/;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend
    location /api {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Scheme \$scheme;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8001/api;
        proxy_redirect off;
    }

    # Admin access (/admin/)
    location /admin {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Scheme \$scheme;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8001\$request_uri;
        proxy_redirect off;
    }

    # Static files
    location /static {
        alias /home/taiga/taiga-back/static;
    }

    # Media files
    location /media {
        alias /home/taiga/taiga-back/media;
    }

    # Events
    location /events {
        proxy_pass http://127.0.0.1:8888/events;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
	}
}
EOF
```

Có thể kiểm tra nginx với câu lệnh `nginx -t`

Cuối cùng restart lại nginx:

```bash
sudo systemctl restart nginx
```

Bây giờ, ta đã có thể truy cập vào địa chỉ taiga để sử dụng.

### 2.5 Cài thêm SSL

Cài Certbot:

```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt install -y python-certbot-nginx
```

Cài SSL cho tên miền `example.com` với câu lệnh

Note: Nếu lần đầu cài Cert, câu lệnh sẽ yêu cầu nhập mail và xác nhận đồng ý điều khoản.

```bash
certbot --nginx -d example.com
# sau đó chọn option 2: điều hướng toàn bộ http sang https
```

Từ đây, ta có thể sử dụng taiga với cert xin từ Let's Encrypt.

## 3. Script cài đặt

Script cài đặt là [taiga-server.sh](./taiga-server.sh)

Script cài đặt Taiga trên server Ubuntu 18.04.



Tajo user taiga:

```bash
# add user taiga
sudo adduser taiga
sudo adduser taiga sudo
echo "taiga ALL=(ALL) NOPASSWD: ALL" > /etc/sudoer.d/taiga
sudo su taiga
```

Download script taiga-server.sh.

Sử dụng: Sửa biến ở đầu script theo yêu cầu.

```console
# domain name of taiga host
TAIGA_DOMAIN="example.com"
```

và chạy script:

```bash
chmod 700 taiga-server.sh
./taiga-server.sh
```

Sau đó cấu hình SSL:

```bash
# install certbot for ssl
add-apt-repository ppa:certbot/certbot -y
apt-get update
apt-get install -y python-certbot-nginx

# install SSL for $TAIGA_DOMAIN
certbot --nginx -d $TAIGA_DOMAIN
```