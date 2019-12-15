# 1. Components of K8s
# 2. Resources of K8s

## 1. Components of k8s

 - **Node**
 
thành phần được xây dựng để chạy trên tất cả các node của cluster, quản lý và báo cáo tình trạng các pod cho cluster.

Có một agent tên là kubelet, quản lý và báo cáo hoạt động các node về API server của master. kubelet sẽ chạy các container sử dụng container runtime như docker. nó ko quản lý container không tạo bởi k8s.

Kube-proxy đảm nhiệm vai trò routing giữa service và các pods.

Mỗi node sẽ có container runtime đảm nhận việc chạy các container. k8s hỗ trợ một vài container runtime như Docker,..
 
<img src="https://i.imgur.com/tpTTzoZ.png"> 

 - **Master**

Quản lý tất cả các hoạt động, thao tác với các container trong cluster. Bao gồm: 

	 API server (kube-apiserver)
	 etcd
	 scheduler (kube-scheduler)
	 controller manager (kube-controller-manager)
	 cloud controller manager (cloud-controller-manager)
    
**API Server** cung cấp các RESTful APIs cho các thành phần khác trong master. Có thể lấy thông tin về một resource trong k8s,theo dõi sự thay đổi của chúng hoặc tạo mới một resource sử dụng các APIs này. API server lưu thông của các đối tượng trongk8s vào etcd.

**etcd** là hệ thống phân tán, mn mở, dùng để lưu trữ các giá trị key-value. K8s dùng etcd để lưu, cập nhật và nhân bản các data của nó.

**scheduler** có nhiệm vụ determine node nào trong cluster có thể sử dụng để chạy pods.

**controller manager** là tập các vòng điều khiển quan sát sự thay đổi từ API server để make sure rằng cluster luôn ở trạng thái mà nó mong muốn.

**cloud controller manager** được sử dụng để tương tác với các cloud provider.

 - **Addons**
 
là các pods và service hiện thực các chức năng của một cluster như DNS server, Web UI (Dashboard) hỗ trợ quản lý k8s bằng giao diện, Container Resource Monitoring (record các thông tin về hệ thống vào database và cho phép chúng ta phân tích các thông tin đó sử dụng UI) và Cluster-level Logging (lưu log của các container để chúng ta có thể xem thông tin log của chúng).

## 2. Resources of K8s

 - **Controllers**
 
1. **Deployment**: là loại chung nhất, muốn deploy một dịch vụ nào đó. Ta tạo pod bằng cách tạo ra một deployment(hoặc statefulSets,..).
2. **DeamonSet**: thường dành cho các dịch vụ cần chạy trên tất cả các node.
3. **StatefulSet**: là 1 file "manifest"(bảng kê khai) đặt trong thư mục chỉ định bởi kubelet, các pod này sẽ được chạy khi kubelet chạy. ko thể điều khiển bằng kubectl.

<img src="https://i.imgur.com/Gl2fROh.png"> 

 - **Replica Sets**
    
 Có nhiệm vụ tạo ra số lượng node giống nhau và duy trì hoạt động của chúng. Giả sử có 1 trong 5 node bị hỏng (chạy dịch vụ), Replica Sets sẽ tạp ra một node khác giống thế và tiếp tục duy trì hoạt động
 
 - **Service**
  
Pod có tuổi thọ ngắn, ko đảm bảo địa chỉ ip luôn cố định => khó khăn cho việc giao tiếp giữa các microservice. Một dịch vụ, một lớp nằm trên các pod được gắn static ip và có thể trỏ domain vào dịch vụ này.(có thể thực hiện load balancing nếu tìm được 5 pods thỏa mãn label)

Thực hiện bởi domain name và port. Service sẽ tự động tìm các pod được đánh label phù hợp (trùng với label của service), rồi chuyển các connection tới đó.

Mỗi service sẽ gắn 1 domain do người dùng chọn, khi cần kết nối đến service, ta chỉ cần dùng domain. Domain được quản lý bởi hệ thống name server SkyDNS nội bộ của k8s.
 
 - **Storage**
 
Pod có thể chỉ định một shared storage volumes. Các container trong pod có thể truy cập vào volume này.
 
  - **Volume**
  
Nơi mà các container có thể truy cập và lưu trữ thông tin.

**Persistent volume** (PV) là khái niệm đưa ra một dung lượng lưu trữ THỰC TẾ 1GB, 10GB,...

**Persistent volume claim** (PVC) là khái niệm ảo, đưa ra một dung lượng cần thiết, mà ứng dụng yêu cầu.

Khi 1PV thỏa mãn yêu cầu của 1 PVC thì chúng "match" nhau, rồi "bound" (buộc/kết nối) lại với nhau.

 - **Storage Classes**
 
Cung cấp một cho quản trị viên cách mô tả các lớp lưu trữ mà họ cung cấp.

 - **Namespaces**
 
Cung cấp một mức độ cô lập với các phần khác của cluster
Svc, pods, replication controller và volumes có thể dễ dàng cộng tác trong cùng một namespace.

 - **ConfigMap (cm) - secret**
 
ConfigMap là giải pháp nhé 1 file config/đặt các ENVironment var hay set các argument khi gọi câu lệnh.
ConfigMap là một cục config, mà pod nào đó cần, giup dễ dàng chia sẻ file cấu hình.

Secret dùng để lưu trữ các mật khẩu, token, ... hay những gì bí mật. Nó nằm trong container.

 - **Labels**
 
là cặp key-value được k8s đính kèm vào pod,rep controllers,...

 - **Networking**
 
Mỗi pod sẽ được cấp 1 ip. Các container trong cùng 1 pod cùng chia sẻ network namespace(địa chỉ ip và port). Các container trong cùng pod có thể giao tiếp vs nhau và có thể giao tiếp với các container ở pod khác (use the shared network resources). 

 - **ingress**
 
Sau khi deploy ứng dụng lên container, để truy cập tới nó chúng ta cần một channel để bên ngoài có thể truy cập được. Channel này là ingress

 - **job**
 
Tạo nên một hoặc nhiều Pod đảm bảo 1 lượng trong số chúng chạy đến khi hoàn thành. Ngay khi hoàn tất, các container sẽ ko được khởi động lại.
Một số trường hợp sử dụng là tải một dữ liệu hàng loạt.

 - **Cronjob**
 
Chạy job theo lịch định sẵn, định dạng lịch định sẵn theo định dạng của Cron trên linux.
Một số trường hợp sử dụng là sao lưu dữ liệu theo lịch.
