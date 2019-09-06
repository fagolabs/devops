CEPH CHEATSHEET
---

## 1. Common Commands

| STT | Mô tả | Command |
| --- | --- | --- |
| 1 | Capture CEPH status | ceph -s |
| 2 | Debug CEPH theo thời gian thực | ceph -w |
| 3 | Get chi tiết tình trạng của CEPH health (pgs, OSDs nào lỗi, etc.) | ceph healh detail |
| 4 | Get ceph osd tree | ceph osd crush tree |
| 5 | List all ceph pools | ceph osd pool ls |


## 2. Troubleshooting command


| STT | Mô tả | Command |
| --- | --- | --- |
| 1 | Set noout cho cụm CEPH | ceph osd set noout |
| 2 | Unset noout cho cụm CEPH | ceph osd unset noout |
| 3 | Out OSD khỏi cụm CEPH| ceph osd out osd.**<osd_id>** |
| 4 | Remove OSD khỏi cụm CEPH | ceph osd purge osd.**<osd_id>** --yes-i-really-mean-it |
| 5 | Tăng tốc độ rebalance data | ceph tell 'osd.*' injectargs '--osd-max-backfills 16' <br> ceph tell 'osd.*' injectargs '--osd-recovery-| max-active 4' |
| 6 | **[LUKS enabled]** List dmcrypt keys | ceph-mon ceph config-key ls <br> Kết quả lệnh là danh sách các dmcrypte key: dm-crypt/osd/**<encrypted_partition_uuid>**/luks |
| 7 | Get OSD ID tương ứng key get được ở mục 6 | ceph osd dump \| grep **<encrypted_partition_uuid>** \| awk '{ print $1 }' |
| 8 | Xác định host tương ứng với một Installs | ceph osd find "$OSD_ID" \| grep host (Trong đó OSD_ID định dạng: **osd.<osd_id>**) |


## 3. Config Ceph Dashboard
Tất cả những câu lệnh trong phần này được thực hiện trong ceph-mon instance.

| STT | Mô tả | Command |
| --- | --- | --- |
| 1 | Liệt kê tất cả các module đang được kích hoạt trên ceph-mgr | ceph mgr module ls
| 2 | Kích hoạt module ceph dashboard trên ceph-mgr | ceph mgr module enable dashboard
| 3 | Show URL truy cập các module trên ceph-mgr | ceph mgr services
| 4 | Kích hoạt cấu hình SSL cho module ceph dashboard | ceph config set mgr mgr/dashboard/ssl true
| 5 | Bỏ kích hoạt cấu hình SSL cho module ceph dashboard | ceph config set mgr mgr/dashboard/ssl false
| 6 | Cấu hình file certificate sử dụng cho SSL của module ceph dashboard trên tất cả các ceph-mgr instance | ceph config-key set mgr mgr/dashboard/crt -i <cert_file_path>
| 7 | Cấu hình file private key sử dụng cho SSL của module ceph dashboard trên tất cả các ceph-mgr instance | ceph config-key set mgr mgr/dashboard/key -i <key_file_path>
| 8 | Cấu hình file certificate sử dụng cho SSL của module ceph dashboard trên một ceph-mgr instance cụ thể | ceph config-key set mgr mgr/dashboard/<ceph-mgr_instance_ID>/crt -i <cert_file_path>
| 9 | Cấu hình file private key sử dụng cho SSL của module ceph dashboard trên một ceph-mgr instance cụ thể | ceph config-key set mgr mgr/dashboard/<ceph-mgr_instance_ID>/key -i <key_file_path>
| 10 | Cấu hình địa chỉ truy cập cho module ceph dashboard trên tất cả các ceph-mgr instance | ceph config set mgr mgr/dashboard/server_addr <IP_address/hostname>
| 11 | Cấu hình port truy cập cho module ceph dashboard trên tất cả các ceph-mgr instance | ceph config set mgr mgr/dashboard/server_port <port_number>
| 12 | Cấu hình địa chỉ truy cập cho module ceph dashboard trên một ceph-mgr instance cụ thể | ceph config set mgr mgr/dashboard/<ceph-mgr_instance_ID>/server_addr <IP_address/hostname>
| 13 | Cấu hình port truy cập cho module ceph dashboard trên một ceph-mgr instance cụ thể | ceph config set mgr mgr/dashboard/<ceph-mgr_instance_ID>/server_port <port_number>
| 14 | Tạo tài khoản đăng nhập trên giao diện module ceph dashboard | ceph dashboard set-login-credentials <username> <password>

| 
