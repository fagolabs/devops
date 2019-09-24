OPENSTACK CHEATSHEET
---

## 1. Cấu hình CPU model cho Openstack

- Trên các Compute Node (các node chạy nova-compute), cấu hình file sau để chỉnh sửa CPU model: ```/etc/nova/nova-compute.conf```

### 1.1 Cấu hình CPU model dpdk-compatible cho các VM
- Trên các Compute Node (các node chạy nova-compute), mở file: /etc/nova/nova-compute.conf. Chỉnh sửa dưới section ```[libvirt]```:

```
[libvirt]
cpu_mode = host-passthrough
```

hoặc

```
[libvirt]
cpu_mode = host-model
```

Thông thường các CPU Intel hiện đại trên các server đều support DPDK nên có thể chọn một trong hay mode cấu hình như trên. Tuy nhiên khi cấu hình nova ở một trong hai mode này, CPU model của VMs sẽ bị fix cứng, dẫn tới việc có thể không live migrate được (vẫn cold migrate OK) sang Compute Host khác (nếu server đích sử dụng CPU model khác)

- Restart lại nova-compute để áp dụng cấu hình: ```systemctl restart nova-compute```

### 1.2 Cấu hình CPU model custom
- Lấy danh sách các CPU model mà KVM hỗ trợ:

```
cat /usr/share/libvirt/cpu_map.xml | grep "model\ name" | awk -F\' '{ print $2 }'
```

Chọn một trong các CPU model mà KVM support, ví dụ: Broadwell, Skylake-Client

- Chỉnh sửa CPU model custom trong file ```/etc/nova/nova-compute.conf```:

```
[libvirt]
cpu_mode = custom
cpu_model = Broadwell
```

- Restart lại nova-compute để áp dụng cấu hình: ```systemctl restart nova-compute```
