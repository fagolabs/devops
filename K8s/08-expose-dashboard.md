# Expose K8s dashboard

Thực hiện expose và hướng dẫn truy cập dashboard

## Mô hình expose

Khi cài đặt với Kubespray, mặc định đã tạo K8s dashboard container và service dạng ClusterIP (không expose ra bên ngoài). Contanier này được tạo với options tự sinh cert cho SSL. Nên để expose dashboard ra ngoài thông qua Ingress, ta thực hiện như sau:
- Sửa lại deployment của K8s dashboard: bỏ việc tự động sinh cert, cấu hình expose qua HTTP
- Sửa lại svc của K8s dashboard: trỏ vào port HTTP
- Tạo Ingress trỏ vào Service của K8s dashboard.

## Các bước thực hiện

### 1. Sửa lại deployment

Mở deployment của K8s dashboard

```bash
kubectl edit -n kube-system deployment kubernetes-dashboard
```

Sửa các thông số sau:
- chuyển tất cả các tham số port từ 8443 thành 9090
- chuyển `livenessProbe` từ HTTPS sang HTTP
- bỏ options "--auto-generate-certificates" và thêm các options sau:
```
- --insecure-bind-address=0.0.0.0
- --insecure-port=9090
- --enable-insecure-login
```
Lưu lại và thoát.

Kiểm tra:

```bash
kubectl get deploy -n kube-system
```

### 2. Sửa lại Service

Mở Service của K8s dashboard

```bash
kubectl edit -n kube-system service kubernetes-dashboard
```

Sửa trường `spec.port`:

```console
ports:
- port: 80
  protocol: TCP
  targetPort: 9090
```

Lưu lại và thoát.

Kiểm tra:

```bash
kubectl get svc -n kube-system
```

### 3. Tạo Ingress cho Dashboard

Các bước tạo Ingress cho dashboard:
- Tạo Issuer trong namespace `kube-system`
- Test thử với staging
- Tạo Ingress với cert Prod

Lưu ý: phải trỏ DNS tên miền của dashboard vào các host trước khi thực hiện

#### 3.1. Tạo Issuer

Issuer chỉ có giá trị trong một namespace, vì kubernetes-dashboard nằm trong kube-system nên phải tạo thêm Issuer:
- Tạo Issuer staging:

```bash
cat > test-issuer.yml << EOF
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
  name: letsencrypt-staging
  namespace: kube-system
spec:
  acme:
    # The ACME server URL
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: user@example.com
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-staging
    # Enable the HTTP-01 challenge provider
    http01: {}
EOF
kubectl apply -f test-issuer.yml
```

- Tạo Issuer prod:

```bash
cat > production-issuer.yml << EOF
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
 name: letsencrypt-prod
 namespace: kube-system
spec:
 acme:
   # The ACME server URL
   server: https://acme-v02.api.letsencrypt.org/directory
   # Email address used for ACME registration
   email: user@example.com
   # Name of a secret used to store the ACME account private key
   privateKeySecretRef:
     name: letsencrypt-prod
   # Enable the HTTP-01 challenge provider
   http01: {}
EOF

kubectl apply -f production-issuer.yml
```

#### 3.2. Test thử với staging

Tạo Ingress với staging cert:

```bash
cat > 01-staging-k8s-dashboard-ingress.yaml << EOF
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-k8s-dashboard-ingress
  namespace: kube-system
  annotations:
    kubernetes.io/ingress.class: "nginx"
    certmanager.k8s.io/issuer: "letsencrypt-staging"
    #certmanager.k8s.io/issuer: "letsencrypt-prod"
    certmanager.k8s.io/acme-challenge-type: http01
    nginx.ingress.kubernetes.io/proxy-body-size: 10m
spec:
  tls:
  #- secretName: test-quickstart-tls
  - secretName: staging-dashboard-k8s-tls
    hosts:
    - ka.fagolabs.tk
  rules:
  - host: ka.fagolabs.tk
    http:
      paths:
      - backend:
          serviceName: kubernetes-dashboard
          servicePort: 80
EOF

kubectl apply -f 01-staging-k8s-dashboard-ingress.yaml
```

Kiểm tra:

```bash
watch -n1 "kubectl get certificate -n kube-system"
```

Chờ đến khi kết quả là `true` thì có thể chuyển sang tạo cert Prod. Nếu chờ quá lâu mà không chuyển thì đã có lỗi xảy ra.

#### 3.3. Tạo cert Prod

Nếu đã tạo thành công cert staging thì chắc chắn sẽ tạo được cert Prod.

Trước hết, xóa Ingress staging:

```bash
kubectl delete -f 01-staging-k8s-dashboard-ingress.yaml
```

Tạo cert Prod:

```bash
cat > 02-prod-k8s-dashboard-ingress.md << EOF
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: prod-k8s-dashboard-ingress
  namespace: kube-system
  annotations:
    kubernetes.io/ingress.class: "nginx"
    #certmanager.k8s.io/issuer: "letsencrypt-staging"
    certmanager.k8s.io/issuer: "letsencrypt-prod"
    certmanager.k8s.io/acme-challenge-type: http01
    nginx.ingress.kubernetes.io/proxy-body-size: 10m
spec:
  tls:
  #- secretName: test-quickstart-tls
  - secretName: prod-dashboard-k8s-tls
    hosts:
    - ka.fagolabs.tk
  rules:
  - host: ka.fagolabs.tk
    http:
      paths:
      - backend:
          serviceName: kubernetes-dashboard
          servicePort: 80
EOF

kubectl apply -f 02-prod-k8s-dashboard-ingress.md
```

Kiểm tra:

```bash
watch -n1 "kubectl get certificate -n kube-system"
```

Khi cert chuyển sang True là đã thành công.

## Truy cập dashboard

Truy cập dashboard K8s thực hiện như sau:
- Tạo người dùng
- Gán quyền cho người dùng
- Lấy token để truy cập

### 1. Tạo người dùng admin

```bash
cat > 03-k8s-dashboard-admin-sa.yaml << EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system
EOF
kubectl apply -f 03-k8s-dashboard-admin-sa.yaml
```

### 2. Gán quyền

```bash
cat > 04-k8s-dashboard-admin-crb.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
EOF
kubectl apply -f 04-k8s-dashboard-admin-crb.yaml
```

### 3. Truy cập vào dashboard

Lấy token để truy cập bằng câu lệnh:

```bash
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
```

Truy cập vào dashboard, chọn xác thực bằng token. Copy nội dung của token vừa lấy được và paste vào đây.
