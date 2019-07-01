# 1. Export Kibana dashboard, visualization, search, index-pattern
- Thực thi script: python elasticsearch_export.py "__elasticsearch url__" "__number of objects to export__". Ví dụ: python elasticsearch_export.py http://127.0.0.1:9200 500
- Chú ý:
  - Sửa giá trị "__elasticsearch url__", nếu không cung cấp giá trị "__elasticsearch url__", mặc định "__elasticsearch url__" là: http://127.0.0.1:9200
  - Sửa giá trị "__number of objects to export__", nếu không cung cấp giá trị "__number of objects to export__", mặc định số lượng object tối đa được export là: 500
  - Mặc định script này sẽ export toàn bộ các objects của ELK stack dưới dạng file json (mỗi object là 1 file json riêng biệt), ra các thư mục riêng với tên tương ứng: dashboard, visualization, search, index-pattern
  - Elasticsearch URL mặc định: http://127.0.0.1:9200

# 2. Import Kibana dashboard, visualization, search, index-pattern
- Thực thi script: python elasticsearch_import.py "__path to json directory__" "__elasticsearch url__". Ví dụ: python elasticsearch_import.py ./dashboard http://127.0.0.1:9200
- Chú ý: 
  - Sửa giá trị "__elasticsearch url__"
  - Thay "__path to json directory__" bằng đường dẫn tới thư mục chứa các templates của dashboard, visualization, search, index-pattern. Script này sẽ tự tìm kiếm các templates định dạng json trong thư mục này và import vào elasticsearch.
  - Nếu không cung cấp hai giá trị "__path to json directory__" và "__elasticsearch url__" thì đường dẫn mặc định là thư mục chứa scripts python và Elasticsearch URL mặc định là http://127.0.0.1:9200
