---
# Cài đặt K8s cluster

### Tổng quan

Cài đặt K8s cluster với Kubespray v2.8.5 trên Ubuntu 18.04.

Kubespray là tool cài K8s bằng ansible nên có thể:
- cài từ một máy ngoài cluster,
- hoặc cài từ một host trong cluster.

### Chuẩn bị môi trường:

##### Cấu hình host và firewall

Các host dùng là Ubuntu 18.04
Mỗi máy cần cài python-apt:

```bash
apt install -y python-apt
```
Cho phép IP forward trên mỗi máy:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Các port cần mở trên firewall, phạm vi là các host trong cluster:
- TCP Port 22: cho phép SSH,
- TCP Port 2379-2380: etcd,
- TCP/UDP Port 6784-6784: control và data port Weave-network,
- (optional) TCP port 6781-6782: thông tin trạng thái của Weave-network,
- giao thức ESP, protocol number 50: fast data-path của Weave,
- TCP port 10250: Kubelet API,
- TCP port 10251: kube-scheduler,
- TCP port 10252: kube-control-manager,
- TCP port 6443: kubernetes api server,
- TCP/UDP port 30000-30010: NodePort.

##### SSH key

Cần cho phép ssh từ host cài đặt tới các node khác trong mạng với key, người dùng sử dụng để ssh phải là sudoer.

### Cài đặt

Download Kubespray vào máy cài đặt

```bash
git clone https://github.com/kubernetes-sigs/kubespray -b v2.8.5
cd kubespray
pip install -r requirements.txt
```

Tạo thư mục config:

```bash
cp -rfp inventory/sample inventory/mycluster
```

Tiếp theo ta khai báo các host sẽ cài đặt trong cluster:

```bash
declare -a IPS=(1.1.1.1 2.2.2.2 3.3.3.3)
CONFIG_FILE=inventory/mycluster/hosts.ini python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```

Ta có thể xem lại file config vừa tạo tại `inventory/mycluster/host.ini` để tinh đặt các host theo ý muốn.

NOTE: thứ tự host trong file config sẽ theo thứ tự khai báo trong biến `IPS`

Sửa network plugin, sửa file `inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml`:

```bash
# Choose network plugin (cilium, calico, contiv, weave or flannel)
# Can also be set to 'cloud', which lets the cloud provider setup appropriate routing
kube_network_plugin: weave
```

Cài K8s:

```bash
ansible-playbook -i inventory/mycluster/hosts.ini -u <ssh-user-name> --private-key=/path/to/key --become --become-user=root cluster.yml
```

Các option cần chú ý:
- tùy chọn `-u <ssh-user-name>`: tên người dùng để ssh tới các host, người dùng này phải là sudoer, người dùng mặc định là người dùng chạy câu lệnh `ansible-playbook`
- tùy chọn  --private-key=/path/to/key, mặc định là key trong `~/.ssh/id_rsa`

NOTE: trong quá trình cài đặt, sẽ có tình huống hết timeout của dịch vụ nào đó, việc này có thể do tốc độ cài đặt chậm, làm cho việc cài đặt failed, tìm tới file `handlers/main.yml` trong folder `roles/<tên thành phần>` điều chỉnh thời gian chờ (delay) và số lần thử lại (retries)

Sau khi cài xong, kiểm tra lại các node đã cài:

```bash
kubectl get nodes
```

Hoàn thành cài đặt K8s bằng Kubespray.

### Thêm, xóa node hoặc reset cluster

**Xóa node**: nếu muốn xóa node2 192.168.2.71 khỏi cluster, sửa file *inventory/mycluster/hosts.ini*

- Trong [all]: giữ tất cả các node

```bash
[all]
node1    ansible_host=192.168.2.70 ip=192.168.2.70
node2    ansible_host=192.168.2.71 ip=192.168.2.71
```
- Trong [kube-node]: chỉ giữ node2

```bash
[kube-node]
node2
```

- Chạy câu lệnh: `ansible-playbook -i inventory/mycluster/hosts.ini remove-node.yml`


**Thêm node**: thêm node2 192.168.2.71 vào cluster, mở file *inventory/mycluster/hosts.ini*
- Trong [all]: thêm node2

```bash
[all]
node1    ansible_host=192.168.2.70 ip=192.168.2.70
node2    ansible_host=192.168.2.71 ip=192.168.2.71
```
- Trong [kube-node]: giữ tất cả các node hoặc chỉ để node2 cũng được

```bash
[kube-node]
node1
node2
```
hoặc

```bash
[kube-node]
node2
```

- Chạy: `ansible-playbook -i inventory/mycluster/hosts.ini scale.yml`

**Reset cluster**: Nếu muốn hủy cluster (khuyên làm khi cài lại cluster hoặc khi bị lỗi khi cài):

```bash
ansible-playbook -i inventory/mycluster/hosts.ini reset.yml
```
