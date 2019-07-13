---
# Cert-manager

[Cert-manager](https://github.com/jetstack/cert-manager) là addon trong K8s, là controller quản lý K8s certificate. Nó có khả năng xin certificate từ nhiều nguồn: Let's Encrypt, HashiCorp Vault... hoặc self-signed cert.

Nó đảm bảo certificate là hợp lệ và tự động xin mới khi cert sắp hết hạn.

Tài liệu hướng dẫn cài đặt và xin Cert từ Let's Encrypt thay vì sử dụng self-signed cert.

### Yêu cầu

1. Cần cài đặt Helm
2. Đã có tên miền trỏ về cluster (host expose Ingress)
3. Cấu hình lại Coredns trong namespace kube-system: Pod chạy Cert-manager cần phải truy cập được các svc ở trong K8s cluster, cũng như có thể kết nối tới Let's Encrypt (địa chỉ ở bên ngoài để xin Cert). Ta sẽ cấu hình lại Coredns có thể phân giải các địa chỉ bên ngoài cluster trước, sau đó là các địa chỉ bên trong cluster (có DNS suffix là `cluster.local`). Từ đây ta có thể cấu hình Pod chạy Cert-manager chỉ cần dùng địa chỉ svc của Coredns.

Trước hết, ta sửa lại config file của Coredns (được gọi là Corefile),

```bash
kubectl edit configmap -n kube-system coredns
```

Thêm nội dung sau vào cấu hình của corefile:

```
...
data:
  Corefile: |
    .:53 {
    	errors
    	health
    	forward . <dns_resolver>:53 {
    	  except cluster.local
    	}
    	hosts {
    		fallthrough
    	}
    	kubernetes ...
    }
...
```

với dns_resolver là địa chỉ của DNS server giúp phân giải tên miền public, VD: 8.8.8.8

```bash

```

### Cài đặt

Để cài đặt bằng Helm chart, trước hết ta cài thêm:

```bash
# Cài thêm một số `CustomResourceDefinition`
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.8/deploy/manifests/00-crds.yaml

# Tạo namespace cho cert-manager
kubectl create ns cert-manager

# Label namespace to disable resources validation
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true

# Thêm jetstack helm repo
helm repo add jetstack https://charts.jetstack.io

# Update Helm chart repository nếu đã cài từ trước
helm repo update

# Lấy địa chỉ IP của Service Coredns và thêm vào danh sách nameservers ở bên dưới
kubectl get svc -n kube-system coredns

#NAME      TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
#coredns   ClusterIP   10.233.0.3   <none>        53/UDP,53/TCP,9153/TCP   11d

# Install the cert-manager Helm chart
cat > values.yaml << EOF
dnsConfig:
  nameservers:
  - 10.233.0.3
dnsPolicy: None
EOF

helm install \
  --name cert-manager \
  --namespace cert-manager \
  --version v0.8.1 \
  -f values.yaml \
  jetstack/cert-manager

```

Check kiểm tra cài đặt, các pod ở trạng thái running là thành công:

```bash
kubectl get po -n cert-manager
```

Cert-manager sử dụng hai custom resources là
- Issuer (hoặc ClusterIssuer): Issuer định nghĩa nơi mà cert-manager sẽ tới để xin TLS cert. Issuer có giá trị trong một namespace, còn ClusterIssuer có giá trị trên cả cluster,
- Certificate: là tài nguyên mà cert-manager sử dụng để cho người dùng biết trạng thái và theo dõi ngày hết hạn của cert.

Ta có thể triển khai production hoặc thử nghiệm (test) với Let's Encrypt. Nhưng Let's Encrypt production rate limits khá nhỏ nên ta nên test trước khi triển khai production.

##### 1. Test (staging)

Email được sử dụng bởi Let's Encrypt để thông báo cho người dùng khi cert sắp hết hạn

```bash
cat > test-issuer.yml << EOF
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
  name: letsencrypt-staging
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

Check trạng thái của Issuer:

```
$ kubectl describe issuer

...
Last Transition Time:  2018-11-17T18:04:00Z
Message:               The ACME account was registered with the ACME server
Reason:                ACMEAccountRegistered
Status:                True
Type:                  Ready
Events:                    <none>
```

Tạo Ingress và cert:

```bash
cat > staging-ingress.yml << EOF
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: kuard
  annotations:
    kubernetes.io/ingress.class: "nginx"    
    certmanager.k8s.io/issuer: "letsencrypt-staging"
    certmanager.k8s.io/acme-challenge-type: http01

spec:
  tls:
  - hosts:
    - gitlab.hieunt79.com
    secretName: quickstart-example-tls
  rules:
  - host: gitlab.hieunt79.com
    http:
      paths:
      - path: /
        backend:
          serviceName: kuard
          servicePort: 80
EOF

kubectl apply -f staging-ingress.yml
```

Cert-manager sẽ tạo ra một CDRs (CustomResourceDefinition) là Certificate:

```bash
kubectl get certificate
```

Check trạng thái của Certificate:

```
$ kubectl describe certificate

 Events:
   Type     Reason          Age                From          Message
   ----     ------          ----               ----          -------
   Normal   CreateOrder     9m                 cert-manager  Created new ACME order, attempting validation...
   Normal   DomainVerified  8m                 cert-manager  Domain "gitlab.hieunt79.com" verified with "http-01" validation
   Normal   IssueCert       8m                 cert-manager  Issuing certificate...
   Normal   CertObtained    7m                 cert-manager  Obtained certificate from ACME server
   Normal   CertIssued      7m                 cert-manager  Certificate issued Successfully
```

Nếu kết quả như trên thì cert đã tạo thành công. Lúc này, Cert-manager đã tạo một secret chứa nội dung của certificate.

```
$ kubectl describe certificate

Name:         quickstart-example-tls
Namespace:    default
Labels:       certmanager.k8s.io/certificate-name=quickstart-example-tls
Annotations:  certmanager.k8s.io/alt-names=gitlab.hieunt79.com
              certmanager.k8s.io/common-name=gitlab.hieunt79.com
              certmanager.k8s.io/issuer-kind=Issuer
              certmanager.k8s.io/issuer-name=letsencrypt-staging

Type:  kubernetes.io/tls

Data
====
tls.crt:  3566 bytes
tls.key:  1675 bytes
```

Lúc này ta có thể triển khai production

##### 2. Production

Tạo Issuer production (chú ý sửa mail):

```bash
cat > production-issuer.yml << EOF
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
 name: letsencrypt-prod
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

Tạo Ingress-production:

```bash
cat > production-ingress.yml << EOF
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: kuard
  annotations:
    kubernetes.io/ingress.class: "nginx"    
    certmanager.k8s.io/issuer: "letsencrypt-prod"
    certmanager.k8s.io/acme-challenge-type: http01

spec:
  tls:
  - hosts:
    - gitlab.hieunt79.com
    secretName: quickstart-example-tls
  rules:
  - host: gitlab.hieunt79.com
    http:
      paths:
      - path: /
        backend:
          serviceName: kuard
          servicePort: 80
EOF

kubectl apply -f production-ingress.yml
```

Tạo Production certificate sẽ lâu hơn staging một chút.

```
$ kubectl get certificate

NAME                     READY 		AGE
quickstart-example-tls   True		3m
```

Lúc này, ta đã truy cập vào dịch vụ của mình với Certificate từ Let's Encrypt.

Muốn sử dụng Issuer staging hay production, ta cần chuyển đổi các trường trong annotations trong Ingress:
