# OS supported: ubuntu 16.04, ubuntu 18.04
# Hướng dẫn build & run SELKS bằng docker
- Bước 1: Setup môi trường docker và python:

  ```
  bash 1-install-docker.sh
  bash 2-python-environment.sh
  ```

- Bước 2: Setup Amsterdam:

  ```
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

- Bước 4: Kiểm tra cài đặt:
  - Sau khi các container của stack SELKS đã tạo xong, cần phải chờ một khoảng thời gian để scirius và moloch khởi động xong dịch vụ.
  - Kiểm tra trạng thái các docker containers:
   
  ```
  docker ps
  ```
  
  - Mở hai console ssh, dùng lệnh watch để theo dõi hai container scririus và moloch:
  
  ```
  watch -n 2.0 "docker logs --tail 20 ams_scirius_1"
  watch -n 2.0 "docker logs --tail 20 ams_moloch_1"
  ```
  
  - Với scirius, đợi cho tới khi có log thông báo như sau nghĩa là đã khởi tạo xong:
  
  ![scririus](images/moloch/1-scirius.png "scirius")
  
  - Với moloch, đợi cho tới khi có log thông báo như sau nghĩa là đã khởi tạo xong:
  
  ![moloch](images/moloch/2-moloch.png "moloch")

- Bước 5: Import Elasticsearch visualization, index-pattern, dashboard, search vào stack SELKS theo mục 3 trong hướng dẫn sau: https://github.com/thaihust/devops/tree/master/selks/utilities/elasticsearch

- Bước 6: Truy cập portal scirius: https://_host ip_. Account mặc định access vào scririus: scirius/scirius

- Bước 7: Cấu hình Kibana portal:

  - Trên giao diện scirius, click vào ô Dashboard để mở Kibana dashboard: 

  ![scirius to kibana](images/kibana/1.png "scirius to kibana")

  - Trên Kibana dashboard, click vào Discover, Kibana sẽ yêu cầu tạo một Index pattern. Nhập: `logstash*` và click Next step.

  ![index pattern](images/kibana/4.png "index pattern")

  - Cấu hình Time Filter là: `@timestamp`. Sau đó click "Create index pattern"

  ![time filter](images/kibana/5.png "time filter")

  - Click lại vào Discover để xem log:

  ![discover](images/kibana/6.png "discover")
