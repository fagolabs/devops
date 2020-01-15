# K8s service provider MVP (rancher/rancher)
## 1. Chuẩn bị trước khi tiến hành cài đặt
## 2. Tiến hành cài đặt rancher
## 3. Tiến hành thêm các node vào rancher
## 4. Triên khai harbor server trên rancher
## 5. Tạo tài khoản người dùng(user)
###	1. Chuẩn bị trước khi tiến hành cài đặt
Trước khi tiến hành cài đặt, ta cần chuẩn bị 2 **node**: 1 **node master** và 1 **node worker**. Bên trong **/etc/host** của **master**, **node** phải có **IP** của nhau, bên cạnh đó cũng cần phải có **docker**, môi trường **kube** cùng với **kubelet**, **kubeadm** và **kubectl**. Chi tiết cách cài đặt có thể tham khảo tại đường **link** sau: **https://github.com/fagolabs/devops/blob/master/K8s/k8s_manual_install.md**.
Trong trường hợp bạn đã có các **host** đã cài đặt **Kubernetes** **(K8s)** từ trước, bạn phải tiến hành **clean** toàn bộ **docker container**, **images** và **volumes**, sau đó cài lại những cái đã đề cập ở trên.
Để **clean** **node** ta nhập câu lệnh:

	docker rm -f $(docker ps -qa)
	docker rmi -f $(docker images -q)
	docker volume rm $(docker volume ls -q)
	
	for mount in $(mount | grep tmpfs | grep '/var/lib/kubelet' | awk '{ print $3 }') /var/lib/kubelet /var/lib/rancher; do umount $mount; done
	
	rm -rf /etc/ceph \
       /etc/cni \
       /etc/kubernetes \
       /opt/cni \
       /opt/rke \
       /run/secrets/kubernetes.io \
       /run/calico \
       /run/flannel \
       /var/lib/calico \
       /var/lib/etcd \
       /var/lib/cni \
       /var/lib/kubelet \
       /var/lib/rancher/rke/log \
       /var/log/containers \
       /var/log/pods \
       /var/run/calico

###	2. Tiến hành cài đặt rancher
- Sau khi chuẩn bị 2 **node**: **kmaster** và **knode**. Cài đặt **rancher** trên **node** **kmaster**.

		sudo docker run -d --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher

Câu lệnh trên sẽ cài đặt **rancher** phiên bản mới nhất. Để tải phiên bản cố định ta thêm **version** vào cuối câu lệnh. Ví dụ như **version 2.3.0** ta thêm **:v2.3.0**.

- Sau khi cài đặt xong ta vào **rancher** theo địa chỉ của **node** cài đặt **rancher**.
	
<img src="https://i.imgur.com/7jg0FyW.jpg">

- Tại đây ta nhập mật khẩu cho tài khoản **admin**.

<img src="https://i.imgur.com/zRMj4AR.jpg">

- Tiếp đến ta chọn **URL** cho **kmaster**, ta có thể dùng **domain name** hoặc địa chỉ **IP** (ở đây ta dùng địa chỉ **IP**).

<img src="https://i.imgur.com/demYmW9.jpg">

Đây là màn hình giao diện của **rancher**.

###	3. Tiến hành thêm các node vào rancher
- Trước tiên ta nhấp vào **Add cluster** ở góc trên bên phải của **rancher**.

<img src="https://i.imgur.com/zkcvdoq.jpg">

<img src="https://i.imgur.com/oTytLWk.jpg">

- Tiếp đó ta chọn **Custom** và nhập tên cho **cluster** ta muốn tạo rồi nhấn **next**.

<img src="https://i.imgur.com/G5pWBnS.jpg">

<img src="https://i.imgur.com/mww0Uem.jpg">

- Sau đó ta sẽ tích vào ô vuông ở mục 1 và copy paste câu lệnh ở mục 2 vào các **node** mà chúng ta muốn **add** vào **cluster**.
**etcd**, **Control Plane**, **Worker** đối với **node** **kmaster** và **Worker** đổi với **node** **knode**.

<img src="https://i.imgur.com/JlHdfPt.jpg">

<img src="https://i.imgur.com/S5YJAkS.jpg">

- Đợi một lúc để các **node** thêm vào **rancher**.
Nhấn **Done** và tiếp tục chờ **cluster** cài đặt.

<img src="https://i.imgur.com/zVH6THz.jpg">	

<img src="https://i.imgur.com/WJpvcG9.jpg">

###	4. Triên khai harbor server trên rancher
- Nhấn vào **Apps** bên trong **default** của **cluster**, sau đó nhấn vào **Launch** và bấm vào **harbor**.

<img src="https://i.imgur.com/A7qwAON.jpg">

- Chọn tên cho **harbor**.

<img src="https://i.imgur.com/TmkO0So.jpg">

- Tại **Harbor Proxy Service Type** chọn **nodePort**.

<img src="https://i.imgur.com/mLlxBVx.jpg">

<img src="https://i.imgur.com/gHKBbDA.jpg">

- Sau đó bấm **Launch** để tiến hành triển khai. Đợi một lúc để cài đặt ứng dụng.
Hình ảnh khi cài đặt thành công.

<img src="https://i.imgur.com/xeXx36i.jpg">

- Chúng ta vào thử **harbor** xem nó có hoạt động không.

<img src="https://i.imgur.com/XZmRE6t.jpg">

- Đăng nhập bằng tài khoản **admin**.

<img src="https://i.imgur.com/73Xaw4c.jpg">

Vậy chúng ta đã triển khai **harbor** thành công trên **rancher**.

###	5. Tạo tài khoản người dùng(user)
- Để tạo tài khoản chúng ta vào **user** ở **Global**.

<img src="https://i.imgur.com/wPMYYEz.jpg">

- Nhấn vào **Add User** để tạo tài khoản.

<img src="https://i.imgur.com/kzy4V44.jpg">

<img src="https://i.imgur.com/UcFDoh2.jpg">

<img src="https://i.imgur.com/ljk3sYM.jpg">

- Dưới đây là một số thông tin để tạo tài khoản, tuỳ vào nhu cầu sử dụng để chọn các mục khác nhau. Ở đây ta tạo một tài khoản **Standard User**.

<img src="https://i.imgur.com/EstAu1Q.jpg">

<img src="https://i.imgur.com/mkoWHVo.jpg">

- Ta sẽ đăng nhập bằng tài khoản **user1**.

<img src="https://i.imgur.com/SKFQZf8.jpg">

- Đây là giao diện của người dùng. Hoàn toàn giống với giao diện của **admin**. Tuy nhiên quyền của tài khoản **user** sẽ hạn chế hơn so với **admin**. Ví dụ trong mục **Users**.

<img src="https://i.imgur.com/4LNatSE.jpg">

Để sử dụng ta có thể làm tương tự các bước ở trên từ tạo **cluster**, thêm **node** cho đến **deploy** ứng dụng hoàn toàn giống với các bước đã trình bày ở phần trên.
