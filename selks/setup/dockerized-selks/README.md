# Hướng dẫn build & run SELKS bằng docker
- Bước 1: Setup môi trường docker và python:

  ```
  bash 1-install-docker.sh
  bash 2-install-docker-compose.sh
  bash 3-python-environment.sh
  ```

- Bước 2: Setup Amsterdam:

  ```
  git clone https://github.com/thaihust/Amsterdam.git
  cd Amsterdam
  python setup.py install
  ```

- Bước 3: Trên thư mục bất kì, generate SELKS docker-compose dùng để cài SELKS:

  ```
  amsterdam -d ams -i eth0 setup
  cd ams
  docker-compose up -d
  ```
