# Triển khai Taiga trên K8s

1. [Cài đặt](#1-Cài-đặt)
2. [Backup](#2-Backup)

## Mô hình cài đặt

Tham khảo [Helm chart](./taiga-helm)

## 1. Cài đặt

Các bước cài đặt:
- Tạo PVC cho taiga
- Cài đặt các thành phần của taiga với Helm
- Expose Taiga qua Ingress

### Tạo PVC cho Taiga

Với cài đặt này của Helm thì để dữ liệu được lưu lại sau mỗi lần restart container thì cần phải tạo PVC trước khi chạy Helm. Cần tạo 3 PVC sau:
- PVC cho Taiga backend
- PVC cho DB
- PVC cho back-up

Ví dụ sử dụng NFS làm storage cung cấp PVC:

```yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: taiga-back-pv
  labels:
    apps: taiga-back
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: "nfs-service.storage.svc.cluster.local"
    path: "/taiga/backend"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: taiga-back-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ""
  resources:
    requests:
      storage: 5Gi
  selector:
    matchLabels:
      apps: taiga-back
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: taiga-db-pv
  labels:
    apps: taiga-db
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: "nfs-service.storage.svc.cluster.local"
    path: "/taiga/db"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: taiga-db-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ""
  resources:
    requests:
      storage: 5Gi
  selector:
    matchLabels:
      apps: taiga-db
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: taiga-backup-pv
  labels:
    apps: taiga-backup
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: "nfs-service.storage.svc.cluster.local"
    path: "/taiga/backup"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: taiga-backup-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ""
  resources:
    requests:
      storage: 1Gi
  selector:
    matchLabels:
      apps: taiga-backup
```

### Cài các Taiga với Helm

Sử dụng [helm chart](./taiga-helm)

```bash
cd devops/K8s/
```

Triển khai

```bash
helm install -f taiga-helm/values.yaml --name taiga ./taiga-helm
```

NOTE: Có thể sử dụng file values.yaml.sample để làm file values.yaml

|Parameter| Description| Default value|
|-|-|-|
|replicaCount|lượng replica cho mỗi thành phần| 1|
|PYTHONUNBUFFERED || 1
|C_FORCE_ROOT || 1
|DJANGO_DB_NAME | DB name của Taiga sử dụng, cần phải giống với POSTGRES_DB| 
|DJANGO_DB_PASSWORD |Password truy cập DB, cần phải giống với POSTGRES_PASSWORD| DB_PASSWORD
|DJANGO_DB_USER |User truy cập DB, cần phải giống với POSTGRES_USER| DB_USER
|DJANGO_SECRET_KEY |secret key, cần phải giống với TAIGA_SECRET| DJANGO_SECRET
|TAIGA_SECRET || DJANGO_SECRET
|POSTGRES_DB || taiga
|POSTGRES_PASSWORD || DB_PASSWORD
|POSTGRES_USER || taiga
|RABBITMQ_DEFAULT_USER || taiga
|RABBITMQ_DEFAULT_PASS || RABBIT_PASS
|RABBITMQ_DEFAULT_VHOST || /taiga
|RABBITMQ_ERLANG_COOKIE || 'ERLANGE_PASS'
|TAIGA_MAX_PRIVATE_PROJECTS_PER_USER | private project tối đa cho một user| 2
|TAIGA_MAX_PUBLIC_PROJECTS_PER_USER |public project tối đa cho một user| 2
|TAIGA_MAX_MEMBERSHIPS_PRIVATE_PROJECTS |số lượng user tối đa mỗi private project| 4
|TAIGA_MAX_MEMBERSHIPS_PUBLIC_PROJECTS |số lượng user tối đa mỗi public project| 4
|TAIGA_HOSTNAME |tên miền của taiga host| MYHOSTNAME
|TAIGA_PUBLIC_REGISTER_ENABLED |cho phép đăng ký người dùng public hay không| false
|TAIGA_SSL |Dùng HTTPS cho taiga| True
|taiga_db_claim |PVC cho DB| taiga-db-pvc
|taiga_volume_claim |PVC cho backend| taiga-back-pvc
|taiga_backup_claim |PVC cho backup| taiga-backup-pvc

Xoá

```bash
helm delete --purge taiga
```

### Expose Taiga qua Ingress

Cách thực hiện:
- Trước hết, tạo Staging cert để kiểm tra
- Deploy Prod nếu staging thành công

#### Tạo staging

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    #certmanager.k8s.io/issuer: "letsencrypt-prod"
    certmanager.k8s.io/issuer: "letsencrypt-staging"
    certmanager.k8s.io/acme-challenge-type: http01
  name: staging-taiga-fagolabs-ingress
  labels:
    app: taiga
spec:
  rules:
    - host: taiga.fagolabs.tk
      http:
        paths:
          - path: /
            backend:
              serviceName: taiga-frontend
              servicePort: 8888
          - path: /api
            backend:
              serviceName: taiga-backend
              servicePort: 8000
          - path: /events
            backend:
              serviceName: taiga-events
              servicePort: 8888
  tls:
      - hosts:
          - taiga.fagolabs.tk
        #secretName: prod-taiga-fagolabs-tls
        secretName: staging-taiga-fagolabs-tls

```


#### Deploy Prod

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    certmanager.k8s.io/issuer: "letsencrypt-prod"
    #certmanager.k8s.io/issuer: "letsencrypt-staging"
    certmanager.k8s.io/acme-challenge-type: http01
  name: prod-taiga-fagolabs-ingress
  labels:
    app: taiga
spec:
  rules:
    - host: taiga.fagolabs.tk
      http:
        paths:
          - path: /
            backend:
              serviceName: taiga-frontend
              servicePort: 8888
          - path: /api
            backend:
              serviceName: taiga-backend
              servicePort: 8000
          - path: /events
            backend:
              serviceName: taiga-events
              servicePort: 8888
  tls:
      - hosts:
          - taiga.fagolabs.tk
        secretName: prod-taiga-fagolabs-tls
```


## 2. Backup

Thực hiện backup các pvc bằng Stash tương tự như Jira và Gitlab, ta backup cho các pvc đã tạo
