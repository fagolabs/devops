# k8s-taiga

A helm chart to deploy taiga.
Works in conjunction with the taiga-container-build
project (which provides the containers).

## Mô hình cài đặt

Helm chart cài đặt Taiga với các thành phần sau:
- Taiga backend: tự build lại image
- Taiga frontend: tự build lại image
- Taiga events: tự build lại image
- Rabbitmq: sử dụng image của google registry
- Postgresql for DB: sử dụng image của google registry
- Redis: sử dụng image của google registry

Tham số được truyền vào dưới dạng biến môi trường, thông qua file [`configmap.yaml`](./templates/configmap.yaml).

Các custom image được build từ thư mục [taiga-container-build](../taiga-container-build)