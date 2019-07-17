---
# Cài đặt và sử dụng Stash để backup và restore stateful Service

## Giới thiệu

Với dịch vụ sử dụng PersistentVolume, ta sẽ có nhu cầu snapshot lại để đảm bảo backup và restore khi có sự cố khi hoạt động, cũng như cho phép di chuyển dịch vụ sang cluster khác.

Có hai công cụ phổ biến để thực hiện yêu cầu trên là Heptio Velero và Stash. Velero (2.8k Github stars) có độ phổ biến cao hơn Stash (580 stars). Tuy nhiên, tài liệu hướng dẫn của Velero cho bare metal K8s rất ít (chỉ support các cloud provider lớn); trong khi đó, Stash hỗ trợ nhiều local storage như NFS, GlusterFS cũng như cloud provider nên Stash sẽ được lựa chọn để triển khai backup và restore PVC.

## Cách hoạt động của Stash

#### Các khái niệm trong Stash:

- Restic: là Custom resource (CRD) trong Kubernetes do Stash định nghĩa và sử dụng. Nó cung cấp khả năng cấu hình cho công cụ [restic](https://restic.net) (công cụ được dùng để backup và restore). Ta chỉ cần mô tả các yêu cầu trong Restic object, Stash theo dõi object này thực hiện các yêu cầu đó
- Repository: cũng là một Custom resource. Khi Stash thực hiện backup bằng restic nó sinh ra một Repository CRD, nó cho phép người dùng theo dõi trạng thái của các backup
- Snapshot: thể hiện một 
- Recovery: là một Custom resource. Cung cấp cấu hình để restore các backup được tạo bới Stash. Người dùng chỉ cần chỉ ra: Repository, Snapshot, đường dẫn và volume muốn restore.

#### Mô hình triển khai

Stash cho phép sử dụng nhiều loại backend để backup, cả on-premise (hostPath, Ceph, GlusterFS, NFS...) và trên cloud (s3, gcs, azure)

#### Hoạt động khi backup

1. Trước hết, người dùng tạo một Secret. ... Nó chứa một password dùng để mã hóa nội dung của backup.
2. Người dùng khi muốn tạo backup, họ cần định nghĩa một `Restic` CRD, bao gồm các thông tin: label để lựa chọn ứng dụng muốn backup, volume nào trên ứng dụng, backend sử dụng để backup.
3. `Stash` operator theo dõi các `Restic` CRD. Khi nó tìm thấy yêu cầu mới, nó sẽ thực hiện tìm kiếm ứng dụng để backup dựa vào nội dung trong Restic.
4. `Stash` thêm một container vào pod hiện tại của ứng dụng, container này có nhiệm vụ sao chép nội dung volume từ trong Pod ra backend ở bên ngoài.
5. container này tạo một `Repository` CRD ở lần backup đầu tiên và định kỳ tạo backup theo yêu cầu trong `Restic`. Người dùng có thể theo trạng thái của backup.

#### Hoạt động khi restore

1. Người dùng tạo một `Recovery` CRD chỉ ra `Repository` họ muốn khôi phục lại. Ngoài ra cần chỉ ra các volume chứa các dữ liệu cần khôi phục.
2. `Stash` operator theo dõi các `Recovery` và check liệu `Repository` trong đó có tồn tại hay không.
3. Nếu có `Stash` tạo một Job để khôi phục data
4. Job đọc thông tin backend từ `Repository` CRD và key mã hóa từ Secret
5. Job thực hiện hồi phục data từ backend và lưu lại vào volume được chỉ định.
6. Người dùng sử dụng volume này để triển khai lại dịch vụ.

## Cài đặt

#### 1. Hướng dẫn cài đặt Stash bằng Helm:

Trong triển khai này sử dụng phiên bản 0.8.1 (phiên bản mới nhất tại tháng 7/2019 0.8.3 bị lỗi khi triển khai)

```bash
helm repo add appscode https://charts.appscode.com/stable/
helm repo update
helm search appscode/stash
helm install appscode/stash --name stash-operator --version 0.8.1 --namespace kube-system
```

Kiểm tra cài đặt:

- Kiểm tra Pod của Stash:

    ```
    $ kubectl get po -n kube-system -l app=stash

    NAMESPACE     NAME                              READY     STATUS    RESTARTS   AGE
    kube-system   stash-operator-859d6bdb56-m9br5   2/2       Running   2          5s
    ```

- Kiểm tra các custom resource:

    ```
    $ kubectl get crd -l app=stash

    NAME                                 AGE
    recoveries.stash.appscode.com        5s
    repositories.stash.appscode.com      5s
    restics.stash.appscode.com           5s
    ```

#### 2. Cài đặt backend để backup

Cài đặt NFS server để làm backend, sử dụng hướng dẫn của [appscode](https://github.com/appscode/third-party-tools/blob/master/storage/nfs/README.md#deploy-nfs-server)

Chú ý cài thêm gói `nfs-common` trên tất cả các node

```bash
apt install -y nfs-common
```

## Backup, restore cho Gitlab, Jira

chi tiết hoạt động backup và restore cho gitlab và jira

#### 1. Gitlab

##### Backup

Tạo secret dùng để chứa mật khẩu truy cập vào snapshot

```bash
echo -n 'gitlab-backup-password' > GITLAB_RESTIC_PASSWORD
kubectl create secret generic gitlab-secret --from-file=./GITLAB_RESTIC_PASSWORD
```

check xem secret đã tạo thành công chưa:

```
kubectl get secret gitlab-secret -o yaml
```

Tạo restic cho Gitlab như sau:

```bash
cat > gitlab-restic.yml << EOF
apiVersion: stash.appscode.com/v1alpha1
kind: Restic
metadata:
  name: gitlab-restic
  namespace: default
spec:
  selector:
    matchLabels:
      app: gitlab-gitlab-ce
  # fileGroups là array gồm các đường dẫn được backup trong Pod
  fileGroups:
  - path: /gitlab-data
    retentionPolicyName: 'keep-last-3' 
  backend:
    local:
      # mountPath có thể đặt là gì cũng đc nhưng đừng trùng với các đường dẫn có sẵn trong Pod muốn backup
      mountPath: /safe/data
      # sử dụng nfs server vừa tạo ở trên làm backend
      nfs:
        # ta có thể để tên miền svc hoặc IP của svc
        server: "nfs-service.storage.svc.cluster.local"
        path: "/"
    storageSecretName: gitlab-secret
  # schedule sử dụng giống hệt cú pháp cron
  # tạo snapshot hàng giờ
  schedule: '@hourly'
  volumeMounts:
  - mountPath: /gitlab-data
    name: gitlab-data
  # chỉ giữ lại 3 snapshot mới nhất
  retentionPolicies:
  - name: 'keep-last-3'
    keepLast: 3
    prune: true
EOF
```

    NOTE: Sau khi tạo restic, một sidecar container được thêm vào deployment của gitlab. Với strategy mặc định, Deployment sẽ xóa pod gitlab cũ rồi mới tạo lại Pod mới (maxUnavailable=1 và ta chỉ có một Pod) gây downtime vài phút, ta có thể sửa tham số như sau:

    ```bash
    kubectl patch deployment gitlab-gitlab-ce --type="merge" --patch='{"spec": {"rollingUpdate": {"maxUnavailable": 0}}}'
    ```

Ta tạo restic để backup cho gitlab:

```bash
kubectl apply -f gitlab-restic.yml
```

Sau vài phút check xem đã có repository và snapshot chưa:

```bash
kubectl get repository
kubectl get snapshot
```

##### Restore



#### 2. Jira

##### Backup

Tạo secret chứa mật khẩu mã hóa

```bash
echo -n 'jira-backup-password' > JIRA_RESTIC_PASSWORD
kubectl create secret generic jira-secret --from-file=./JIRA_RESTIC_PASSWORD
```

Tạo restic cho Jira như sau:

```bash
cat > jira-restic.yml << EOF
apiVersion: stash.appscode.com/v1alpha1
kind: Restic
metadata:
  name: jira-restic
  namespace: default
spec:
  selector:
    matchLabels:
      app: atlassian-jira-software
  fileGroups:
  - path: /var/atlassian/jira
    retentionPolicyName: 'keep-last-3' 
  backend:
    local:
      mountPath: /safe/data
      nfs:
        server: "nfs-service.storage.svc.cluster.local"
        path: "/jira"
    storageSecretName: gitlab-secret
  schedule: '@hourly'
  volumeMounts:
  - mountPath: /var/atlassian/jira
    name: jira-data
  retentionPolicies:
  - name: 'keep-last-3'
    keepLast: 3
    prune: true
EOF
```

## Tham khảo:
- https://appscode.com/products/stash/0.8.3/setup/install/
- https://github.com/appscode/third-party-tools/blob/master/storage/nfs/README.md
- https://appscode.com/products/stash/0.8.3/guides/backup/