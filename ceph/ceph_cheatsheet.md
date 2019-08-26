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

## 3. 
