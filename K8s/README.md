# Cài đặt Kubernetes Cluster on-premise và triển khai dịch vụ Gitlab, Jira


### Các bước thực hiện:

1. Cài đặt Kubernetes cluster với Kubespray: [01-k8s-with-kubespray](./01-k8s-with-kubespray)
2. Cài đặt GlusterFS + Heketi để cung cấp PVC cho các ứng dụng [02-gluster-heketi](./02-gluster-heketi.md)
3. Cài các tiện ích và add-on cho Kubernetes:

	- Cài Ingress và Helm: [03-k8s-ingress-helm](./03-k8s-ingress-helm.md)
	- Cài Cert-manager: [03-cert-manager](./03-cert-manager.md)

4. Triển khai Gitlab [04-helm-gitlab-ce](./04-helm-gitlab-ce.md)
5. Triển khai Jira [05-hlem-jira](./05-hlem-jira.md)
6. Backup và restore dịch vụ bằng Stash [06-backup-restore](./06-backup-restore.md)