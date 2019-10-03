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

## 2. Common OpenStack operation commands

### 2.1 Keystone (Identity Service)

| Description | Command |
| --- | --- |
| List all users  | keystone user-list |
| List Identity service catalog | keystone catalog |
| List all services in service catalog  | keystone service-list |
| Create new user  | keystone user-create --name NAME --tenant-id TENANT --pass PASSWORD --email EMAIL --enabled BOOL |
| Create new tenant  | keystone tenant-create --name NAME --description "DESCRIPTION" --enabled BOOL |

openrc

### 2.2 Glance (Image Service)

| Description | Command |
| --- | --- |
| List images you can access | glance image-list |
| Delete specified image | glance image-delete IMAGE |
| Describe a specific image | glance image-show IMAGE |
| Update image  | glance image-update IMAGE |

### 2.3 Nova (Compute Service)

| Description | Command |
| --- | --- |
| List all users  | keystone user-list |

### 2.4 Neutron (Networking Service)


| Description | Command |
| --- | --- |
| Create network   | neutron net-create NAME |
| Create a subnet   | neutron subnet-create NETWORK_NAME CIDR <br> neutron subnet-create my-network 10.0.0.0/29|
| List network and subnet   | neutron net-list<br> neutron subnet-list|
| Examine details of network and subnet   | neutron net-show ID_OR_NAME_OF_NETWORK <br> neutron subnet-show ID_OR_NAME_OF_NETWORK|

### 2.5 Cinder (Block Storage Service)

| Description | Command |
| --- | --- |
| __Manage volumes & volume snapshots__ | |
|  Create a new volume   |cinder create SIZE_IN_GB --display-name NAME <br> cinder create 1 --display-name MyFirstVolume  |
|  Boot an instance and attach to volume | knova boot --image IMAGE --flavor FLAVOR --nic net-id=NETWORKID INSTANCE_NAME <br> nova boot --image cirros-qcow2 --flavor m1.tiny 
--nic net-id=3d706957-7696-4aa8-973f-b80892ff9a95 MyVolumeInstance |
|  List volumes, notice status of volume | cinder list |
|  Attach volume to instance after instance is active, and volume is available   | nova volume-attach INSTANCE_ID VOLUME_ID auto <br> nova volume-attach MyVolumeInstance /dev/vdb auto |
| __Manage volumes after login into the instance__ | |
|  List storage devices  | fdisk -l |
|  Make filesystem on volume  | mkfs.ext4 /dev/vdb |
|  Create a mountpoint  | mkdir /myspace |
|  Mount the volume at the mountpoint  | mount /dev/vdb /myspace |
|  Create a file on the volume  | touch /myspace/helloworld.txt <br> ls /myspace |
|  Unmount the volume  | umount /myspace |