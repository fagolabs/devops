# Jira

Cài Jira sử dụng bản đóng gói của [int128](https://github.com/int128/devops-kompose/tree/master/atlassian-jira-software)

```bash
git clone https://github.com/int128/devops-kompose
cd devops-kompose/atlassian-jira-software
cat < jira-values.yml >>EOF
# https://github.com/cptactionhank/docker-atlassian-jira-software

image:
  repository: cptactionhank/atlassian-jira-software
  tag: 7.10.1
  pullPolicy: IfNotPresent

jira:
  reverseProxyHost: jira.domain.tk
  reverseProxyPort: 443
  reverseProxyScheme: https
  javaHeapSize: 1024m
  javaMemoryOptions: "-XX:MaxMetaspaceSize=512m -XX:MaxDirectMemorySize=10m"
  javaOptions: ""

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: false
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  path: /
  hosts:
    - jira.example.com
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

persistence:
  enabled: true
  accessMode: ReadWriteOnce
  size: 5Gi
  storageClass: "slow"
  # existingClaim: existing-pvc

resources: {}

nodeSelector: {}

tolerations: []

affinity: {}
EOF

cd ..
helm install -f atlassian-jira-software/values.yaml --name jira ./atlassian-jira-software
```
