---
# Cài đặt GlusterFS

Cài đặt GlusterFS và Heketi để cung cấp storage-class cho K8s.

Phần cài đặt này sử dụng người dùng `root` và đứng ở thư mục `/root`.

## Điều kiện tiên quyết

Ta cần 3 node trong GlusterFS clustser, mỗi node thêm ít nhất một disk ngoài disk chạy OS.

Trên các node chạy GlusterFS:
- Enable module `dm_thin_pool` trong kernel:

```bash
modprobe dm_thin_pool
```

- Cài GlusterFS client (sử dụng phiên bản `gluster4u0_centos7`):

```bash
add-apt-repository ppa:gluster/glusterfs-4.0 -y
apt update
apt install -y glusterfs-client=4.0.2-ubuntu2~bionic1
```

## Cài đặt

Download Heketi v9.0.0

```bash
git clone https://github.com/heketi/heketi -b v9.0.0
cd heketi/extras/kubernetes
```

Cài glusterfs daemon, thay vì bản latest sẽ dùng bản stable để tránh lỗi:

```bash
sed -i 's/latest/gluster4u0_centos7/g' glusterfs-daemonset.json
kubectl create -f glusterfs-daemonset.json
```

Gắn nhãn cho các node muốn cài lên, ở đây node1,2,3 là tên các node sẽ cài lên:

```bash
kubectl label node node1 storagenode=glusterfs
kubectl label node node2 storagenode=glusterfs
kubectl label node node3 storagenode=glusterfs
```

Tạo service account cho heketi:

```bash
kubectl create -f heketi-service-account.json
```

Cấp quyền heketi điểu khiển glusterfs pod:

```bash
kubectl create clusterrolebinding heketi-gluster-admin --clusterrole=edit --serviceaccount=default:heketi-service-account
```

Tạo Secret chứa cấu hình cho heketi:

```bash
kubectl create secret generic heketi-config-secret --from-file=./heketi.json
```

Trước khi cài tiếp, đợi cho đến khi các pod trong glusterfs daemonset chạy ổn định.

```bash
$ kubectl get pod | grep glusterfs
glusterfs-f6ccc                                 1/1     Running            0          2d15h
glusterfs-f8xv7                                 1/1     Running            0          2d15h
glusterfs-zx6c7                                 1/1     Running            0          20h
```

Tạo initial Pod và Service để truy cập vào nó:

```bash
sed -i 's/dev/9/g' heketi-bootstrap.json
kubectl create -f heketi-bootstrap.json
```

Và chờ cho tới khi heketi-bootstrap pod chạy.

```bash
kubectl get pod -o wide | grep deploy-heketi
```

Tới đây, ta đã có các pod GlusterFS chạy trên các node storage và pod heketi-bootstrap, ta tiến hành tạo file miêu tả topology của GlusterFS. File `topology.json` chứa thông tin về các node, disk trong cluster. Ví dụ dưới đây là topo của cluster gồm 3 node, mỗi node có một disk. Chú ý, tên của node đặt trong `manage`, ip đặt trong `storage`, devices là các disk trên node đó, muốn sử dụng trong GlusterFS.

```json
{
    "clusters": [
        {
            "nodes": [
                {
                    "node": {
                        "hostnames": {
                            "manage": [
                                "node1"
                            ],
                            "storage": [
                                "192.168.2.70"
                            ]
                        },
                        "zone": 1
                    },
                    "devices": [
                        "/dev/vdb"
                    ]
                },
                {
                    "node": {
                        "hostnames": {
                            "manage": [
                                "node2"
                            ],
                            "storage": [
                                "192.168.2.71" 
                            ]
                        },
                        "zone": 1
                    },
                    "devices": [
                        "/dev/vdb"
                    ]
                },{
                    "node": {
                        "hostnames": {
                            "manage": [
                                "node3"
                            ],
                            "storage": [
                                "192.168.2.72" 
                            ]
                        },
                        "zone": 1
                    },
                    "devices": [
                        "/dev/vdb"
                    ]
                }
            ]
        }
    ]
}
```
Sau khi chuẩn bị file mô tả cluster, ta cập nhật file này lên heketi server trong pod `heketi-bootstrap` đang chạy ở trên.

Forward port ra localhost

```bash
kubectl port-forward `kubectl get po| grep heketi| awk '{print $1}'` 8888:8080
```

Mở một terminal khác để kết nối tới heketi server. Download heketi client tương ứng với version của heketi server, ở ví dụ này đang cài đặt theo verison 9:

```bash
cd ~
wget https://github.com/heketi/heketi/releases/download/v9.0.0/heketi-client-v9.0.0.linux.amd64.tar.gz
tar xvzf heketi-client-v9.0.0.linux.amd64.tar.gz
cd heketi-client/bin
export HEKETI_CLI_SERVER=http://localhost:8888
```

Copy file topology đã tạo ở trên vào thư mục hiện tại và chạy câu lệnh update topology `./heketi-cli topology load --json=topology.json`. Trước khi chạy câu lệnh này, cần lường trước các lỗi có thể gặp phải như sau:

- chưa cài các điều kiện bắt buộc ở phần mở đầu
- lỗi kết nối giữa các pod glusterfs daemonset
Biểu hiện:
Ta có thể check kết nối giữa chúng bằng câu lệnh:

```bash
kubectl exec -ti `kubectl get pod -o wide| grep glusterfs| grep node1| awk '{print $1}'` -- gluster peer status

# Number of Peers: 2
# 
# Hostname: node1
# Uuid: bf5a00aa-24cd-4e80-8822-ca88328bed20
# State: Peer in Cluster (Connected)
# 
# Hostname: node3
# Uuid: 4a6876aa-a1c3-4979-8eb7-2d52dc9016d6
# State: Peer in Cluster (Connected)
# Other names:
# 192.168.2.72
```

Nếu `Number of peer` là 0 thì ta cần kết nối thủ công

Workaround:

```bash
# thực hiện kết nối thủ công với mỗi node trong GlusterFS
kubectl exec -ti `kubectl get pod -o wide| grep glusterfs| grep node1| awk '{print $1}'` -- gluster peer probe node2 
kubectl exec -ti `kubectl get pod -o wide| grep glusterfs| grep node1| awk '{print $1}'` -- gluster peer probe node3
kubectl exec -ti `kubectl get pod -o wide| grep glusterfs| grep node2| awk '{print $1}'` -- gluster peer probe node3
```

- Lỗi pod glusterfs không nhận disk, ta phải tự gắn disk vào pod:

Biểu hiện: treo tại adding devices

```bash
heketi-cli topology load --json=topology-sample.json
Creating cluster ... ID: 763d9c28bb1cbfbda46c9888f0398936
     Creating node server-node-02 ... ID: cc0b10651a082a324395ffa12818744e
          Adding device /dev/sdb ... ^C
```

Workaround: Thực hiện trên tất cả các node và với tất cả các disk.

```bash
kubectl exec -ti `kubectl get pod -o wide| grep glusterfs| grep node1| awk '{print $1}'` -- pvcreate --metadatasize=128M --dataalignment=256K /dev/vdb
    Physical volume "/dev/vdb" successfully created.
```

Bây giờ, ta có thể load topology lên heketi server:

```bash
./heketi-cli topology load --json=topology.json

        Found node master1 on cluster d911c804f871193ead91d5a5c3a18439
                Adding device /dev/vdb1 ... OK
        Found node master2 on cluster d911c804f871193ead91d5a5c3a18439
                Adding device /dev/vdb1 ... OK
        Found node master3 on cluster d911c804f871193ead91d5a5c3a18439
                Adding device /dev/vdb1 ... OK
```

Tạo database cho heketi

```bash
./heketi-cli setup-openshift-heketi-storage
```

Câu lệnh trên thực hiện thành công sẽ sinh ra file `heketi-storage.json`. Ta cần chạy file này và đợi cho job thực hiện xong.

```bash
sed -i 's/dev/9/g' heketi-storage.json
kubectl create -f heketi-storage.json
watch -n.5 "kubectl get pod -o wide| grep copy-job"
```

Sau khi job chạy xong, ta xóa các pod bootstrap và cài heketi server thực sự.

```bash
kubectl delete all,service,jobs,deployment,secret --selector="deploy-heketi"
cd ~/heketi/extras/kubernetes
sed -i 's/dev/9/g' heketi-deployment.json
kubectl create -f heketi-deployment.json
```

Ta đã hoàn thành cài đặt glusterfs và heketi làm storage class trong Kubernetes.

## Sử dụng
Tạo storage-class

```bash
cat > storage-class.yml <<EOF
apiVersion: storage.k8s.io/v1beta1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://IP-ADDRESS-OF-HEKETI-SERVICE:8080"
EOF
kubectl create -f storage-class.yml
```

Tạo PVC:

```bash
cat > test-pvc.yml<<EOF
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: myclaim
  annotations:
    volume.beta.kubernetes.io/storage-class: "slow"
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
EOF

kubectl create -f test-pvc.yml
watch -n.5 "kubectl get pvc"
```


## Tham khảo:
- https://blog.lwolf.org/post/how-i-deployed-glusterfs-cluster-to-kubernetes/
