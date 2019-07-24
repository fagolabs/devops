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

- Bước 3: Trên thư mục bất kì, generate SELKS docker-compose file và run SELKS stack:

  ```
  amsterdam -d ams -i eth0 setup
  cd ams
  docker-compose up -d
  ```

  Chú ý thay giá trị eth0 bằng card mạng mà suricata muốn sniff

- Bước 4: Import Elasticsearch visualization, index-pattern, dashboard, search vào stack SELKS theo hướng dẫn ở link sau: https://github.com/fagolabs/devops/tree/master/selks/utilities/elasticsearch. Trong repo này đã có sẵn scripts & các thư mục chứa dashboards, visualizations, index-patterns, searches dành cho SELKS, sẵn sàng để sử dụng.
