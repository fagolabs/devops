# BÁO CÁO THỰC TẬP TỪ XA

| Người hướng dẫn: | Anh Dũng |
| --- | --- |
|   | Anh Thái |
| Người thực hiện: | Vũ Tuấn Bảo |

#

|
## Hà Nội, ngày 10 tháng 12 năm 2019
 |
| --- |

# **MỤC LỤC**

Contents

**MỤC LỤC**         2

Contents        2

1. Kubernetes        3

	1.1 Tổng quan về kubernetes        3

		1.1.1 Kubernetes là gì        3

		1.1.2 Ưu điểm và các tính năng của Kubernetes        3

		1.2.3 Các đối tượng trong Kubernetes        5

	2.1 Triển khai hệ thống kubernetes        7

		2.1.1 Cài đặt trên cả kmaster and knode        7

		2.1.2 Chỉ cấu hình trên kmaster        11

		2.1.3 Cấu hình trên node        13

	3.1 Chạy thử ứng dụng        17

		3.1.1 Tạo ứng dụng web server với image là nginx trên K8S.        17

## 1. Kubernetes

##         1.1 Tổng quan về kubernetes

###                 1.1.1 Kubernetes là gì

 Kubernetes (còn được gọi là k8s) là một hệ thống điều phối container mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng. Ban đầu nó được thiết kế bởi Google và hiện nay đang được duy trì bởi tổ chức Cloud Native Computing Foundation

Nó nhằm mục đích cung cấp một &quot;nền tảng để tự động hóa việc triển khai, mở rộng và vận hành các container chứa ứng dụng trên các cụm máy chủ&quot;. Nó hoạt động với một loạt các công cụ container, bao gồm Docker.

<img src="https://i.imgur.com/c1vlUfU.jpg"> 

###                 1.1.2 Ưu điểm và các tính năng của Kubernetes

<img src="https://i.imgur.com/GwEsRzo.png"> 

- **Endpoint slices** : Theo dõi và mở rộng (scale) các node trên Kobernetes Cluster
- **Load balancing** : Kubernetes cung cấp cho các Pod địa chỉ IP riêng và một DNS duy nhất cho một nhóm Pods. Vì vậy có thể cân bằng tải giữa chúng.
- **Automatic bin packing** : Tự động đặt các container dựa trên yêu cầu tài nguyên của chúng và các ràng buộc khác, để tăng cường sử dụng và tiết kiệm nhiều tài nguyên hơn.
- **Storage orchestration** : Tự động gắn hệ thống lưu trữ mà bạn chọn, cho dù từ bộ nhớ cục bộ (local), nhà cung cấp đám mây như GCP hoặc AWS hoặc hệ thống lưu trữ mạng như NFS, iSCSI, Gluster, Ceph, Cinder hoặc Flocker.
- **Self-healing** : Khởi động lại các container bị dừng, thay thế và sắp xếp lại các container khi các node die, xóa bỏ container bị hỏng.
- **Automated rollouts and rollbacks**
- **IPv4/IPv6 dual-stack** : Phân bổ địa chỉ IPv4, IPv6 tới các Pods và Services
- **Batch execution** : Ngoài các dịch vụ, Kubernetes có thể quản lý Batch, CI, thay thế các container bị dừng.
- **Horizontal scaling** : Scale (mở rộng) ứng dụng của bạn lên hoặc xuống tùy theo mức độ sử dụng CPU

###                 1.2.3 Các đối tượng trong Kubernetes

<img src="https://i.imgur.com/RoJh9ly.png"> 

**Node**

Một node là một máy ảo hoặc máy vật lý chạy Kubernetes. Nodes hay còn gọi là docker host.

**Pods**

là 1 nhóm (1 trở lên) các container thực hiện một mục đích nào đó, như là chạy software nào đó. Nhóm này chia sẻ không gian lưu trữ, địa chỉ IP với nhau. Pod thì được tạo ra hoặc xóa tùy thuộc vào yêu cầu của dự án.

**Replica Sets**

đảm nhận vai trò tạo ra số lượng Pods giống nhau dựa vào yêu cầu và luôn luôn duy trì số lượng đó.
Giả sử quy định replicas: 3 thì nó sẽ tạo ra 3 Pods giống nhau, giả sử 1 pod ở Node (server) nào đó bị sự cố, nó sẽ tạo ra 1 Pod mới để duy trì số lượng là 3 như yêu cầu lúc đầu.

**Services**

Kubernetes Services là một tập hợp các pods hoạt động cùng nhau, chẳng hạn như một lớp của ứng dụng nhiều tầng. Tập hợp các nhóm tạo thành một dịch vụ được xác định bởi một bộ chọn nhãn (Label Selector). Kubernetes cung cấp hai chế độ quản lý dịch vụ, sử dụng biến môi trường hoặc sử dụng Kubernetes DNS.

**Volumes**

Mặc định, các hệ thống tệp tin (File System) trong Kubernetes Container không bền. Điều này có nghĩa là việc khởi động lại pod sẽ xóa sạch mọi dữ liệu trên các container đó và do đó, hình thức lưu trữ này khá hạn chế sử dụng. Vì vậy, Kubernetes cung cấp một giải pháp khác là Volumes để lưu trữ vĩnh viễn dữ liệu trong suốt vòng đời của pod. Nó có thể được chia sẻ giữa các container với nhau trong cùng một Pod. Một Volume sẽ được mount vào container bởi một mount point được định nghĩa trong config của pod.

**Namespaces**

Kubernetes cung cấp phân vùng các tài nguyên mà nó quản lý thành các tập hợp không chồng lấp được gọi là Namespace. Chúng được thiết kế để sử dụng trong các môi trường có nhiều người dùng trải rộng trên nhiều nhóm hoặc dự án hoặc thậm chí tách các môi trường như phát triển (dev), thử nghiệm (test) và sản xuất (Production).

**Deployment**

là việc định nghĩa policy update/phân phối của Replica Set. Nghĩa là sao, là nó sẽ quy định Pods gồm những container nào, các Pods được tạo ra sẽ phân phối đến các Nodes nào trong Kubernetes.

##         2.1 Triển khai hệ thống kubernetes

_Lưu ý: Trước khi cài phải chỉnh CPU trong setting \&gt;=2_

###                 2.1.1 Cài đặt trên cả kmaster and knode

B1: Cập nhật kho lưu trữ

	sudo su

	apt-get update

B2: Tắt swap space

	swapoff -a

	nano /etc/fstab

Thêm # vào trước dòng /swaplife

<img src="https://i.imgur.com/T2kDiVx.png">
 
B3: Cập nhật hostname

	nano /etc/hostname

<img src="https://i.imgur.com/KBZKNRF.png">

B4: Ghi chú lại ip

	apt install net-tools

	ifconfig

<img src="https://i.imgur.com/mrdLssr.png"> 

B5: Cập nhật hosts file

	nano /etc/hosts

<img src="https://i.imgur.com/WxS63jY.png"> 

B6: Khởi động lại và kiểm tra

<img src="https://i.imgur.com/KpelO4B.png">
 
B7: Cài đặt openssh server

	sudo apt-get install openssh-server

B8: Cài đặt docker và môi trường kube

	sudo su

	apt-get update

	apt install curl

	curl -fsSL https://get.docker.com -o get-docker.sh

	sh get-docker.sh

	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

	cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
	deb http://apt.kubernetes.io/ kubernetes-xenial main
	EOF

	add-apt-repository \
  	"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  	$(lsb_release -cs) \
  	stable"

	cat > /etc/docker/daemon.json <<EOF
	{
  	 "exec-opts": ["native.cgroupdriver=systemd"],
  	 "log-driver": "json-file",
  	 "log-opts": {
    	   "max-size": "100m"
  	 },
  	 "storage-driver": "overlay2"
	}
	EOF


	mkdir -p /etc/systemd/system/docker.service.d

	systemctl daemon-reload

	systemctl restart docker

	apt-get update

B9: Cài đặt kubelet, kubeadm và kubectl

	apt-get install -y kubelet kubeadm kubectl

B10: Cập nhật cấu hình kubernetes

	nano /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

Thêm vào dòng dòng sau

	Environment=”cgroup-driver=systemd/cgroup-driver=cgroupfs”

<img src="https://i.imgur.com/xAPIZns.png">
 
B11: Cấp quyền cho docker

	systemctl enable docker.service

###                 2.1.2 Chỉ cấu hình trên kmaster

B1: Chạy câu lệnh

	kubeadm init --apiserver-advertise-address=<ip-address-of-kmaster-vm> --pod-network-cidr=192.168.0.0/16

<img src="https://i.imgur.com/uZjRHD9.png"> 

Hiển thị trên màn hình

<img src="https://i.imgur.com/3EqFEkY.png">
 
B2: Như hình trên, chạy các câu lệnh với tư cách người dùng non-root

	mkdir -p $HOME/.kube
	sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
	sudo chown $(id -u):$(id -g) $HOME/.kube/config

Màn hình hiển thị như dưới là đã chạy thành công

<img src="https://i.imgur.com/ULY4pSY.png"> 

B3: Để kiểm tra xem nó hoạt động hay không, chạy câu lệnh

	kubectl get pods -o wide --all-namespaces

<img src="https://i.imgur.com/t6oXHdq.png"> 

<img src="https://i.imgur.com/eiEeI6e.png"> 

B4: Sửa lỗi coredns

	kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

B5: Cài đặt CALICO pod network

	curl https://docs.projectcalico.org/v3.9/manifests/calico.yaml -O

	POD_CIDR="<your-pod-cidr>" \
	sed -i -e "s?192.168.0.0/16?$POD_CIDR?g" calico.yaml

	kubectl apply -f calico.yaml

B6: Cài đặt dashbord

	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta6/aio/deploy/recommended.yaml

B7: Kiểm tra lại

<img src="https://i.imgur.com/kWn1Y6H.png"> 

<img src="https://i.imgur.com/KsMFc9t.png"> 

###                 2.1.3 Cấu hình trên node

 Copy dòng lệnh nhóm để cấu hình trên node ( root-user)

	kubeadm join 192.168.1.41:6443 --token xfoncu.xnzi3oxr98h6e5qd \
    --discovery-token-ca-cert-hash sha256:9b94650dc8dfd68dc7b4128c6da87f481f6467e44f861398e21c5253ba9e9a11
 
<img src="https://i.imgur.com/uOAvliT.png">

- Để kiểm tra ta dùng câu lệnh

( Chạy dưới quyền non-root user  trên kmaster)

	kubectl get nodes

<img src="https://i.imgur.com/B5Ej4ZC.png">

Vậy là node đã join thành công

- Chạy dòng lệnh trên kmaster

	kubectl proxy

   Nhập vào trang web

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

   Và màn hình xuất hiện

<img src="https://i.imgur.com/34kptyB.png">

   Lấy token

	kubectl create serviceaccount dashboard -n default

	kubectl create clusterrolebinding dashboard-admin -n default \
 	 --clusterrole=cluster-admin \
  	 --serviceaccount=default:dashboard

	kubectl get secret $(kubectl get serviceaccount dashboard -o jsonpath="{.secrets[0].name}") -o jsonpath="{.data.token}" | base64 --decode

<img src="https://i.imgur.com/XGdO08q.png"> 

Nhập token vào trang web

<img src="https://i.imgur.com/NKIh3CQ.png">

<img src="https://i.imgur.com/r8lvmYO.png">

<img src="https://i.imgur.com/D7KT8bc.png"> 

Vậy là đã cài đặt thành công kubernetes.

##         3.1 Chạy thử ứng dụng

###                 3.1.1 Tạo ứng dụng web server với image là nginx trên K8S.

   Bước 1: Tạo các container

Tạo 02 container với images là nginx, 2 container này chạy dự phòng cho nhau, port của các container là 80

	kubectl run test-nginx --image=nginx --replicas=2 --port=80

<img src="https://i.imgur.com/KT2Ny7K.png">

Ta có thể kiểm tra lại các container nằm trong các POD

	kubectl get pods -o wide

<img src="https://i.imgur.com/G71jbxw.png"> 

Ngoài ra ta có thể sử dụng lệnh để dưới để xem các service nào đã sẵn sàng để deployment.

	kubectl get deployment

<img src="https://i.imgur.com/sN9I5Wl.png"> 

   Bước 2: Thực hiện deploy ứng dụng trên

Tới bước này, chúng ta chưa thể truy cập vào các container được, cần thực hiện thêm bước deploy các container với các tùy chọn phù hợp, cụ thể như sau

	kubectl expose deploy test-nginx --port 80 --target-port 80 --type NodePort

<img src="https://i.imgur.com/twh6Pp2.png">

Quan sát kỹ hơn ứng dụng web server vừa tạo ở trên bằng lệnh

	kubectl describe service test-nginx

<img src="https://i.imgur.com/cXabTYc.png">

Đứng trên node kmaster thực hiện curl vào một trong các IP sau:

	curl 10.96.0.103
	hoặc
	curl 192.168.177.193
	hoặc
	curl 192.168.177.194

<img src="https://i.imgur.com/tyDDMGX.png">

Đứng trên node k8s-master và thực hiện kiểm tra port được ánh xạ với container (trong kết quả trên là port 30418/TCP)

	ss -lan | grep 30418

Đứng trên máy Laptop hoặc máy khác cùng dải mạng với dải IP của node trong cụ K8S, mở trình duyệt web và truy cập với địa chỉ: http:// 192.168.1.46:30418

<img src="https://i.imgur.com/QR5DdP4.png">

Kiểm tra trên kubernetes

<img src="https://i.imgur.com/VlmhN7k.png">

Vậy là hệ thống ứng dụng chạy ổn định trên kubernetes

Bài trên đã deploy thành công web server nginx trên k8s. Có thể truy cập thông qua địa chỉ 192.168.1.46:30418 đối với các máy có cùng dải mạng với node trong K8S. Ngoài ra ta còn theo dõi được trên k8s workload status của ứng dụng trên k8s. Sắp tới em sẽ tìm hiểu và triển khai hệ thống zimbra mail server trên k8s ạ.

Trên đây là bài báo cáo của em ạ.

Em cảm ơn các anh ạ.
