# Triển khai Taiga trên K8s

1. [Cài đặt](#1-Cài-đặt)
2. [Backup](#2-Backup)

## 1. Cài đặt

Sử dụng helm chart https://github.com/hieunt79/k8s-taiga

```bash
git clone https://github.com/hieunt79/k8s-taiga -b v0.1.1
```

Triển khai

```bash
helm install -f k8s-taiga/values.yaml --name taiga ./k8s-taiga
```

NOTE: Có thể sử dụng file values.yaml.sample để làm file values.yaml

Xoá

```bash
helm delete --purge taiga
```

Lưu ý khi triển khai:
- Tạo các PVC bằng tay nếu muốn persistent storage, tham khảo pvc.yaml.sample
- Tạo Ingress sau khi chạy Helm vì trong Helm repo không có Ingress, tham khảo file mẫu trong helm repo

## 2. Backup

Thực hiện backup các pvc bằng Stash tương tự như Jira và Gitlab, ta backup cho các pvc đã tạo
