
#	K8s service provider MVP

##	1. Cài đặt Rancher
##	2. Cấu hình Kiểm soát truy cập Rancher
##	3. Thêm máy chủ mới
##	4. Triển khai harbor trên rancher
##	5. Hướng dẫn sử dụng dịch vụ rancher cho user


###	 1. Cài đặt Rancher
Câu lệnh để cài đặt **Rancher**

	sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server

<img src="https://i.imgur.com/1824v98.png"> 

###  2. Cấu hình Kiểm soát truy cập Rancher
Sau đó vào **ADMIN** rồi vào **Access control**, chọn **local** rồi tạo tài khoản **ADMIN**.
Hình ảnh sau khi tạo thành công. 
 
<img src="https://i.imgur.com/2k0NRvk.png"> 

###  3. Thêm máy chủ mới

Sau đó ta chọn phần **add host** để add thêm host. Ban đầu nó sẽ hỏi URL đăng ký máy chủ
http://localhost:8080 hay http://ip:8080 (http://192.168.1.145:8080). Chúng ta chọn dùng ip ở đây.  Đó chính là địa chỉ web của ta.
 
<img src="https://i.imgur.com/0Rac3c0.png"> 
 
Ta chọn **Custom**, nhập địa chỉ ip vào mục 4 và copy dòng lệnh ở mục 5 va paste vào node để chúng connect tới **Rancher server**.
Chúng ta vào **host** trong **INFRASTRUCTURE** để kiểm tra.
 
<img src="https://i.imgur.com/hBd3Ccq.png">  
 
###  4. Triển khai harbor trên rancher
Di chuyển tới **CATALOG** chọn **community**.
 
<img src="https://i.imgur.com/hwu4R59.png">  
 
Gõ **Harbor** vào ô **Search**.
 
<img src="https://i.imgur.com/0U9czC4.png">  
 
Click vào **View Details**, và điền các thông tin cần thiết vào.
 
<img src="https://i.imgur.com/w2yF0Tc.png">  
 
Tiến hành cài đặt.
Sau đó thêm **label** cho host như trong hình. 
 
<img src="https://i.imgur.com/SfHXC9K.png">
<img src="https://i.imgur.com/76rOr2Y.png"> 
<img src="https://i.imgur.com/2A6C0mp.png"> 
 
Vậy là ta đã cài đặt thành công.
Ta truy cập theo đường link: **192.168.1.213** và kết quả nhận được:
 
<img src="https://i.imgur.com/VRBjzWs.png">
<img src="https://i.imgur.com/1Oj5JsY.png"> 
<img src="https://i.imgur.com/qoidyaZ.png"> 

###  5. Hướng dẫn sử dụng dịch vụ rancher cho user
Để tài khoản cho user, ta vào **Account**, chon **Add Account**. 

<img src="https://i.imgur.com/nQVzJCQ.png"> 
<img src="https://i.imgur.com/IdR9t9S.png"> 
 
Vào một **host** (có cùng mạng LAN do đây không phải ip public), truy cập vào đường link **192.168.1.145:8080** để truy cập đến **Rancher**.

<img src="https://i.imgur.com/Gue4uiH.png"> 
<img src="https://i.imgur.com/RLIvaNL.png"> 
<img src="https://i.imgur.com/dwqXRND.png"> 

Đầu tiên chúng ta nhấn vào **Add a host**  màu trắng ở góc trên để thêm **host**.

<img src="https://i.imgur.com/vYouzse.png"> 

Ở đây ta chọn **Custom** (có thể chọn các tùy chọn khác nếu như bạn có tài khoản )Ta nhập địa chỉ host ở mục 4, sau đó copy mục 5 và paste vào **Terminal** để thêm **host** vào **rancher**.

<img src="https://i.imgur.com/mPKydeV.png"> 
<img src="https://i.imgur.com/xFowch4.png"> 
<img src="https://i.imgur.com/H9wEPad.png"> 

Để xem các dịch vụ có thể deploy trên **rancher**, ta chọn **CATALOG** rồi chọn **all**.

<img src="https://i.imgur.com/GIJBdBv.png"> 

Để deploy một dịch vụ nào đó ta nhập tên vào ô **Search**, sau đó bấm vào **View Details**. Ta làm ví dụ đối với **Ghost**.

<img src="https://i.imgur.com/5vPS5BD.png"> 
<img src="https://i.imgur.com/qoHBPZ3.png"> 
<img src="https://i.imgur.com/XDBNLWu.png"> 

Chờ một lúc để dịch vụ cài đặt. 

<img src="https://i.imgur.com/X7ubANY.png"> 

Vậy là đã cài đặt xong. Ta bấm vào **host** trong **INFRASTRUCTURE** để xem dịch vụ deploy trên host nào (trong trường hợp có nhiều **host** và tùy theo yêu cầu của từng dịch vụ).

<img src="https://i.imgur.com/Kxq426D.png"> 

Tiếp đến, ta kiểm tra xem dịch vụ có hoạt động không bằng cách vào bằng địa chỉ ip của host **192.168.0.105** (Tùy vào từng dịch vụ mà ta có các cách vào khác nhau).

<img src="https://i.imgur.com/0oZvNYU.png"> 

Vậy là ta đã deploy dịch vụ thành công trên rancher dưới bằng account user. Ngoài ra, để xem thông tin chi tiết về dịch vụ nào đó ta nhấn **STACKS** rồi nhấn **All**.

<img src="https://i.imgur.com/bIs274K.png"> 

Sau đó nhấn vào tên dịch vụ mà mình muốn xem (ở đây ta nhấn vào **ghost**).
 
<img src="https://i.imgur.com/cCJa6Gz.png"> 
 
Để xem chi tiết hơn nữa ta nhấn vào từng cái bên trong ta nhấn vào tên của chúng.

<img src="https://i.imgur.com/mk7vt5M.png"> 

Không những thế ta còn có thể xem **Link Graph** hoặc **Compose YAML** bằng cách nhấn vào ô biểu tượng bên trong mỗi stack để xem.

<img src="https://i.imgur.com/9sB4Rvq.png"> 
<img src="https://i.imgur.com/VzaDHF4.png"> 
<img src="https://i.imgur.com/vMaSpYB.png"> 

Trên đây là bài hướng dẫn sử dụng rancher k8s cho user.
