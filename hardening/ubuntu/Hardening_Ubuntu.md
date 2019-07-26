# Hardening Ubuntu server

Giới thiệu: các tips, tricks giúp tăng cường an toàn thông tin cho Ubuntu server

Contents:
1. [Người dùng và mật khẩu](#1-Người-dùng-và-mật-khẩu)
2. [Cấu hình SSH](#2-Cấu-hình-SSH)
3. [Quản lý package](#3-Quản-lý-package)
4. [Network, dịch vụ và Iptables](#4-Network,-dịch-vụ-và-Iptables)
5. [Disk và partition](#5-Disk-và-partition)
6. [Logging](#6-Logging)
7. [Các phần mềm cài thêm](#7-Các-phần-mềm-nên-cài-thêm)

## 1. Người dùng và mật khẩu

#### 1.1. Mật khẩu

Nếu tài khoản của người dùng sử dụng mật khẩu, đảm bảo:
- độ dài tối thiểu 12 ký tự, gồm một hoặc hai từ không có trong từ điển
- bao gồm cả chữ hoa, chữ thường, số, ký tự đặc biệt.

Không đặt mật khẩu trùng nhau hoặc gần giống nhau cho các root user trên các hệ thống khác nhau.

Ta có thể sử dụng script sau để tạo mật khẩu.

```bash
cat > /usr/bin/randpw << EOF
#!/bin/bash
password=$(cat /dev/urandom | tr -dc 'A-Za-z0-9@$%^*-=,.'| head -c 16)
echo "$password"
EOF

# cat /dev/urandom : tạo random string
# tr -dc 'A-Za-z0-9@$%^*-=,.' : khai báo charset sử dụng
# head -c 16: cắt lấy chiều dài mong muốn
# echo "$password": in ra terminal để quan sát và lưu lại

chmod 755 /usr/bin/randpw

randpw
```

#### 1.2. Check người dùng không có mật khẩu

Người dùng không có mật khẩu sẽ không đảm bảo an toàn, check những người dùng không có mật khẩu:

```bash
cat /etc/shadow | awk -F: '($2==""){print $1}'
```
#### 1.3. Khóa tài khoản

Nếu tài khoản không đang không sử dụng, có thể khóa lại bằng câu lệnh:

```bash
passwd -l accountName
```

Mở khóa người dùng.

```bash
passwd -u accountName
```

#### 1.4. Đảm bảo chỉ có người dùng root có UID bằng 0

Người dùng có UID bằng 0 có quyền truy cập cao nhất tới hệ thống. Trong đa số trường hợp chỉ nên có một người dùng như vậy (người dùng root). Liệt kê những người dùng có UID bằng 0:

```bash
awk -F: '($3=="0"){print}' /etc/passwd
```

#### 1.5. Cấu hình sudoer

Sudo package cho phép người dùng thường có thể chạy các câu lệnh với tư cách của root. File cấu hình là `/etc/sudoers`, tuy nhiên ta nên sửa thông qua câu lệnh `visudo`. Format chung của file này như sau:

```console
%www ALL=(ALL)NOPASSWD:/bin/cat,/bin/ls

# %www – tất cả người dùng trong nhóm
# ALL= – Từ tất cả Host/IP
# (ALL) – có thể chạy với như tất cả người dùng khác
# NOPASSWD – không yêu cầu password (bỏ trường này thì sẽ yêu cầu password)
# :/bin/cat,/bin/ls – Các câu lệnh được chạy, trong trường hợp này là “cat” và “ls”
```

#### 1.6. Đặt timeout cho user sessions

Ta có thể cấu hình tự động thoát terminal nếu không tương tác trong một khoảng thời gian bằng cách: sửa file `/etc/profile` và thêm biến `TMOUT=300` (tự logout sau 5 phút) và lưu lại.

## 2. Cấu hình SSH

Cấu hình SSH để tăng cường an toàn cho server. File cấu hình của SSH là file `/etc/ssh/sshd_config`

#### Disable root login

Chuyển thành:

```console
PermitRootLogin no
```

#### Chỉ cho phép một số user

```console
AllowUsers accountName
```

#### Chỉ cho phép một số IP được ssh tới

```console
AllowUsers @2.3.4.5
```

#### Kết hợp cả IP và user

```console
AllowUsers accountName@2.3.4.5
```

#### Cho phép groupuser ssh tới

```console
AllowGroups groupname
```

#### Chuyển sang port không phải default

```console
Port 2222
# hoặc bất kì port nào khác
```

#### Không cho phép sử dụng Empty password

```console
PermitEmptyPasswords no
```

#### Sử dụng ssh key thay vì dùng mật khẩu

https://www.linode.com/docs/security/authentication/use-public-key-authentication-with-ssh/

Sau khi cấu hình xong, restart lại tiến trình sshd.

```bash
service sshd restart
```

## 3. Quản lý các package

Tối thiểu các package cài đặt trên server, và cập nhật các bản vá cho các package.

#### 3.1. Tối thiểu các package

Xóa một package và giữ file cấu hình:

```bash
apt remove <package_name>
```

Xóa package và cả các file cấu hình của nó:

```bash
apt remove --purge <package_name>
```

Loại bỏ các dependencies package không còn sử dụng:

```bash
apt-get --purge autoremove
```

#### 3.2. Check các package không sử dụng và loại bỏ

Liệt kê các package đã cài

```bash
dpkg --list
```

Gỡ package bằng các câu lệnh đã liệt kê ở trên.

#### 3.3. Update system

Update phiên bản mới của các package trên system để đảm bảo các bản vá luôn được cập nhật:

Check các bản cập nhật mới:

```bash
sudo apt-get update
```

Nếu muốn cập nhật tất cả các package:

```bash
sudo apt-get upgrade
```

Nếu chỉ muốn cập nhật một vài package:

```bash
apt-get install <package1> <package1>
```

Cân nhắc cho phép tự động cập nhật security update:

```console
$ sudo apt-get install unattended-upgrades
$ sudo dpkg-reconfigure -plow unattended-upgrades

$ cat /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
//  "${distro_id}:${distro_codename}-updates";
//  "${distro_id}:${distro_codename}-proposed";
//  "${distro_id}:${distro_codename}-backports";
};
// Unattended-Upgrade::Mail "my_user@my_domain.com";
```

## 4. Network, dịch vụ và Firewall

#### 4.1. Kiểm tra các dịch vụ đang expose port ra ngoài:

Càng ít port hoạt động thì càng an toàn cho server, sử dụng câu lệnh sau để kiểm tra các port đang hoạt động và tiến trình đi kèm với nó. Nếu chương trình không cần thiết, ta nên ngừng chương trình đó lại.

```bash
netstat -plunt
# hoặc
ss -plunt
```

#### 4.2. Kiểm tra các dịch vụ đang hoạt động

Kiểm tra các dịch vụ đang hoạt động bằng câu lệnh sau, với các dịch vụ bắt đầu bằng **[ + ]** là các dịch vụ đang chạy.

```bash
service --status-all
```

Stop dịch vụ:

```bash
service stop <service_name>
```

Quản lý việc dịch vụ tự động chạy khi khởi động:

```bash
# Disable việc chạy tự động
systemctl disable <service_name>

# cho phép khởi động cùng Host
systemclt enable <service_name>
```

#### 4.3. Harden /etc/sysctl.conf

`/etc/sysctl.conf` là file cho phép thay đổi cấu hình của linux kernel đang chạy. Bằng cách thay đổi một số cấu hình mặc định ta có thể tăng sự an toàn server.

NOTE: Các cấu hình trên có thể ảnh hưởng tới hoạt động của một vài triển khai, nên đọc kĩ hơn trước khi áp dụng vào server của mình.

Thêm các dòng sau vào trong file /etc/sysctl.conf

```console
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1
# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0 
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0
# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
# Block SYN attacks
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5
# Log Martians
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0 
net.ipv6.conf.default.accept_redirects = 0
# Ignore Directed pings
net.ipv4.icmp_echo_ignore_all = 1
```

Sau khi thay đổi, cập nhật vào kernel bằng câu lệnh:

```bash
sysctl -p
```

Check cấu hình của một parameter:

```bash
sysctl <parameter_name>
```

In ra các cấu hình hiện tại của sysctl:

```bash
sysctl -a
```

Đọc kĩ hơn về các options có thể cấu hình trong `/etc/sysctl.conf` tại [đây](https://www.cyberciti.biz/files/linux-kernel/Documentation/networking/ip-sysctl.txt)

#### 4.4. Sử dụng các dịch vụ có mã hóa trên thay vì plain text

Khi liên lạc giữa các máy tính nếu sử dụng các dịch vụ không mã hóa sẽ rất dễ dàng để nghe lén thông tin. Thay vì sử dụng ftp, telnet/rsh, chuyển sang dùng sftp và ssh

#### 4.5. Disable IPv6 nếu không sử dụng

Disable IPv6 bằng GRUB, mở `/etc/default/grub` và sửa các dòng sau:

```console
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash ipv6.disable=1"
GRUB_CMDLINE_LINUX="ipv6.disable=1"
```

đóng file và chạy câu lệnh update:

```bash
sudo update-grub
```

IPv6 sẽ vẫn bị disable sau khi reboot. Để enable IPv6, mở `/etc/default/grub` và sửa lại như cũ:

```console
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""
```

Update lại GRUB:

```bash
sudo update-grub
```

#### 4.6. Sử dụng ufw

Ufw hay Uncomplicated Firewall là giao diện của Iptables được cài đặt mặc định trên các distro gần đây của Ubuntu. Iptables là công cụ mạnh nhưng khá phức tạp với người mới sử dụng. Ta có thể sử dụng `ufw` để cấu hình Iptables cho ubuntu server, dưới đây là một vài sử dụng đơn giản:
- Set policy mặc định:

```bash
# chặn incoming
sudo ufw default deny incoming

# cho phép outgoing
sudo ufw default allow outgoing
```
- Cho phép ssh, `ufw` sử dụng file `/etc/services` để chuyển đổi tên dịch vụ thành port, ta có thể sử dụng:

```bash
sudo ufw allow ssh
# hoặc
sudo ufw allow 22
```
- Tương tư cho phép http và https:

```bash
sudo ufw allow http
sudo ufw allow https
``` 
- Enable ufw: để ufw hoạt động ta cần enable nó:

```bash
sudo ufw enable
```
- Allow Port range:

```bash
sudo ufw allow 6000:6007/tcp
sudo ufw allow 6000:6007/udp
```

Tham khảo thêm tại: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04

## 5. Disk và partition

#### 5.1. Disable usb

Ngăn việc gắn USB vào ubuntu server:

```bash
sudo echo "blacklist uas" >> /etc/modprobe.d/blacklist.conf
sudo echo "blacklist usb-storage" >> /etc/modprobe.d/blacklist.conf
```

Để enable trở lại:

```bash
sed -i '/blacklist uas/d' /etc/modprobe.d/blacklist.conf
sed -i '/blacklist usb-storage/d' /etc/modprobe.d/blacklist.conf
```

#### 5.2. Chia riêng các filesystem vào phân vùng khác nhau

Chia các filesystem vào các phân vùng khác nhau giúp tăng tính an toàn cho hệ thống:
- /usr
- /home
- /var
- /tmp

Bên cạnh đó, tạo riêng filesystem cho apache và FTP server root. Thêm các cấu hình sau vào cấu hình phân vùng trong `/etc/fstab`:
- `noexec`: không cho phép set bit execution cho binaries trên phân vùng này (nhưng cho phép scripts)
- `nodev`: không cho phép sử dụng các file như /dev/zero, hoặc thiết bị /dev/sda trên phân vùng này (không cho phép gắn thêm)
- `nosuid`: 

Ví dụ với phân vùng của FTP server:

```console
/dev/sda5  /ftpdata          ext3    defaults,nosuid,nodev,noexec 1 2
```

#### 5.3. Loại bỏ các file có SUID và SGID không mong muốn

Một file trong linux system thuộc sở hữu của người tạo ra nó. Tương tự như vậy với các tiến trình, nó sẽ chạy với UID và GID của người dùng khởi động nó. Nhưng nếu setuid được dùng, tiến trình không chạy như trên mà chạy với quyền của người dùng sở hữu file thực thi đó. Nó rõ ràng là một mối nguy hiểm nếu không được sử dụng đúng cách.

Tìm kiếm các file với SUID và SGID được bật:

```bash
#See all set user id files:
find / -perm +4000
# See all group id files
find / -perm +2000
# Or combine both in a single command
find / \( -perm -4000 -o -perm -2000 \) -print
find / -path -prune -o -type f -perm +6000 -ls
```

Nên kiểm tra lại nguồn gốc các file và loại bỏ các file bất thường.

#### 5.4. Kiểm tra các file có thể ghi tự do trên linux

Tìm kiếm các file cho phép ghi tự do trong linux

```bash
find /dir -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print
```

Cần kiểm tra và sửa lại permission.

#### 5.5. Tìm kiếm các file không thuộc user hoặc group

```bash
find /dir -xdev \( -nouser -o -nogroup \) -print
```

## 6. Logging

Log file giúp người quản trị theo dõi việc xâm nhập của attacker. Theo dõi và quản lý log file là một việc cực kì quan trọng khi triển khai hệ thống.

#### 6.1. Các câu lệnh để xem log file

Các câu lệnh thường dùng để xem log:
- cat: in ra toàn bộ nội dung file
- tail: thường dùng `tailf` hoặc `tail -f` để liên tục cập nhật các thay đổi
- grep: lọc những nội dung mong muốn
- less, more: xem nội dung của file

#### 6.2. Thư mục chứa log file

Tham khảo thêm tại: https://www.plesk.com/blog/featured/linux-logs-explained/

#### 6.3. Sử dụng logrotate để quản lý log file

Tham khảo tại: https://www.digitalocean.com/community/tutorials/how-to-manage-logfiles-with-logrotate-on-ubuntu-16-04

## 7. Các phần mềm nên cài thêm

#### 7.1. Sử dụng các Intrusion Detection System (IDS)

Network Intrusion Detection System là các công cụ giúp phát hiện xâm nhập hoặc tấn công mạng:
- DDoS
- port scans
- crack password
- ...

Các công cụ IDS phổ biến hiện nay có thể lựa chọn là:
- Snort
- Suricata
- Bro
- OSSEC
- Fail2ban

#### 7.2. Quét rootkit

Quét nhanh các rootkit đã biết:

```bash
apt isntall -y rkhunter
rkhunter -C
```

