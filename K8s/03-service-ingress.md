# Ingress cho các dịch vụ

```bash
cat > service-ingress.yml <<EOF
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: jira-ingress
spec:
  rules:
  - host: jira.domain.tk
    http:
      paths:
      - backend:
          serviceName: jira-svc
          servicePort: 8080
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: tcp-services
  namespace: ingress-nginx
data:
  10222: "default/gitlab-gitlab-ce:22"
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: gitlab-ingress
spec:
  rules:
  - host: gitlab.domain.tk
    http:
      paths:
      - backend:
          serviceName: gitlab-svc
          servicePort: 8080
OEF

kubectl apply -f service-ingress.yml
```
