# OPENSTACK CHEATSHEET

## Contents
### [1. Cấu hình CPU model cho Openstack](#_1)

  * #### [ 1.1 Cấu hình CPU model dpdk-compatible cho các VM](#_11)

  * #### [1.2 Cấu hình CPU model custom](#_12)

### [2. OpenStack commands cheatsheet](#_2)

  * #### [2.1 Keystone - Identity Service](#_21)

  * #### [2.2 Glance - Image Service](#_22)

  * #### [2.3 Nova - Compute Service](#_23)

  * #### [2.4 Neutron - Networking Service](#_24)

  * #### [2.5 Cinder - Block Storage Service](#_25)

---
<a name="_1"></a>
## 1. Cấu hình CPU model cho Openstack

- Trên các Compute Node (các node chạy nova-compute), cấu hình file sau để chỉnh sửa CPU model: ```/etc/nova/nova-compute.conf```

<a name="_11"></a>
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

<a name="_12"></a>
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

<a name="_2"></a>
## 2. OpenStack commands cheatsheet

<a name="_21"></a>
### 2.1 Keystone (Identity Service)

| Description | Command |
| --- | --- |
| List all users  | openstack user list |
| List all services in service catalog  | openstack service list |
| Create new user  | openstack user create --domain default --password demo_user_password demo |
| Create new project  | openstack project create --domain default --description "Demo Project" demo |
| Create role | openstack role create _guest_ |
| Assign a role for user on a project| openstack role add --project demo --user demo _guest_ |
| Create openrc file |cat << EOF > demo-openrc <br> export OS_PROJECT_DOMAIN_NAME=default<br>export OS_USER_DOMAIN_NAME=default<br>export OS_PROJECT_NAME=demo<br>export OS_USERNAME=demo<br>export OS_PASSWORD=demo_user_password<br>export OS_AUTH_URL=http://controller:5000/v3<br>export OS_IDENTITY_API_VERSION=3<br>export OS_IMAGE_API_VERSION=2<br>EOF|
| Source openrc file before executing openstack commands| source demo-openrc<br>openstack endpoint list|

<a name="_22"></a>
### 2.2 Glance (Image Service)

| Description | Command |
| --- | --- |
| List images you can access | openstack image list |
| Delete specified image | openstack image delete <image_id> |
| Describe a specific image | openstack image show <image_id> |

<a name="_23"></a>
### 2.3 Nova (Compute Service)

| Description | Command |
| --- | --- |
|__Manage compute service__||
| List nova services| openstack compute service list|
| List hypervisors | openstack hypervisor list|
| Discover new compute host (add compute host to hypervisor list)| nova-manage cell_v2 discover_hosts --verbose|
| Disable/Enable compute service| _Disable compute service:_<br>openstack compute service set --disable HYPERVISOR_HOSTNAME nova-compute<br><br>_Enable compute service:_<br>openstack compute service set --enable HYPERVISOR_HOSTNAME nova-compute|
|__Common__||
| List flavors   | openstack flavor list |
| Create flavor |openstack flavor create --ram 2048 --disk 20 --vcpus 2 2C.2R.20D |
| List instances, notice status of instance  | openstack server list |
| Show details of instance | openstack server show INSTANCE_NAME_OR_ID<br>e.g:<br>openstack server show ubuntu_vm |
| Login to instance   | ip netns <br> ip netns exec NETNS_NAME ssh -i PATH_TO_SSH_PRIVATE_KEY USER@SERVER<br>e.g:<br>ip netns exec qdhcp-6021a3b4-8587-4f9c-8064-0103885dfba2 ssh -i ubuntu_private_key.pem ubuntu@10.0.0.2|
|  View console log of instance  | openstack console log show INSTANCE_NAME|
| __Pause, suspend, stop, resize, rebuild, reboot an instance__  | |
| Pause  | openstack server pause INSTANCE_NAME |
| Unpause  | openstack server unpause INSTANCE_NAME |
| Suspend  | openstack server suspend INSTANCE_NAME |
| Unsuspend  | openstack server resume INSTANCE_NAME |
| Stop  | openstack server stop INSTANCE_NAME |
| Start  | openstack server start INSTANCE_NAME |
| Reboot  | _Soft reboot:_<br>openstack server reboot INSTANCE_NAME<br><br>_Hard reboot_:<br>openstack server reboot --hard INSTANCE_NAME|
| Resize  | __Step 1:__ Execute resize command:<br>openstack server resize --flavor FLAVOR_NAME INSTANCE_NAME<br>__Step 2:__ Check instance status<br>openstack server list \| grep INSTANCE_NAME<br>__Step 3:__ When the resize completes, the instance status becomes __VERIFY_RESIZE__. Then, confirm resize instance: <br>openstack server resize --confirm INSTANCE_NAME_OR_ID<br>__Step 4:__ If the resize fails or does not work as expected, you can revert the resize:<br>openstack server resize --revert INSTANCE_NAME_OR_ID|
|__Inject a keypair into an instance and access the instance with that keypair__||
|Create keypair | openstack keypair create --public-key HLC_WP_KEY.pub --private-key HLC_WP_KEY.pem HLC_WP_KEY<br> chmod 600 HLC_WP_KEY.pem|
|Use ssh to connect to the instance |ip netns exec qdhcp-98f09f1e-64c4-4301-a897-5067ee6d544f ssh -i HLC_WP_KEY.pem ubuntu@10.0.0.2|
|__Migrate instance__||
|Live migration| __Step 1:__ List available compute hosts and hypervisors<br>openstack compute service list<br>openstack hypervisor list<br>__Step 2:__ Live migrate instance to a specific compute host<br>openstack server migrate INSTANCE_NAME_OR_ID --live HYPERVISOR_HOSTNAME<br>__Step 3:__ If live migration fails or does not work as expected, abort live migration:<br>- Get migration id:<br>nova server-migration-list INSTANCE_NAME_OR_ID<br>- Abort migration:<br>nova live-migration-abort INSTANCE_NAME_OR_ID MIGRATION_ID|
|Cold migration | __Step 1:__ Execute migrate command:<br>openstack server migrate INSTANCE_NAME<br>This command gonna stop instance and launch instance in a new compute host<br>__Step 2:__ Check instance status<br>openstack server list \| grep INSTANCE_NAME<br>__Step 3:__ When the instance migration completes, the instance status becomes __VERIFY_RESIZE__. Then, confirm resize instance: <br>openstack server resize --confirm INSTANCE_NAME_OR_ID<br>__Step 4:__ If the cold migration fails or does not work as expected, you can revert the migration/resize:<br>openstack server resize --revert INSTANCE_NAME_OR_ID|
|__Manage security groups__|__WIP__|

<a name="_24"></a>
### 2.4 Neutron (Networking Service)


| Description | Command |
| --- | --- |
| List network and subnet   | openstack network list<br>openstack subnet list|
| Examine details of network and subnet   | openstack network show <network_id><br>openstack subnet show <subnet_id>|
|List port|openstack port list|
|Create port and attach port to an instance|openstack port create --network <network_name_or_id> --fixed-ip subnet=<subnet_name_or_id>,ip-address=<ip_address> <port name><br>openstack server add port <server_name_or_id> <port_name_or_id>|
|__Capture, sniff traffic on Neutron ports__|__Step 1:__ Get instance IPs and the compute host (hypervisor host) where instances are launched: <br>openstack server show INSTANCE_NAME_OR_ID \| egrep "(hypervisor_hostname\|addresses)"<br>__Step 2:__ Get port id: <br>openstack port list \| grep INSTANCE_IP <br><br>- Port ID will be like this: __db02263e-b433-411b-bd83-d396e5f3f607__<br>- Save shortened port ID: __db02263e-b4__ <br>__Step 3:__ SSH into Compute Host (got from step 1). Capture traffic on neutron port: <br>tcpdump -nni tap<shortended_port_id> <br>e.g: <br>tcpdump -nni tapdb02263e-b4 |

<a name="_25"></a>
### 2.5 Cinder (Block Storage Service)

| Description | Command |
| --- | --- |
| __Manage volumes & volume snapshots__ | |
| Check cinder volume & snapshot status| openstack volume list<br>openstack volume snapshot list |
| Check cinder services status| openstack volume service list|
| Create a new volume   |cinder create SIZE_IN_GB --display-name NAME <br>e.g:<br>cinder create 100 --display-name DATA_VOLUME  |
| Attach volume to instance after instance is active, and volume is available  | openstack server add volume INSTANCE_NAME VOLUME_NAME<br>e.g:<br>openstack server add volume demo_instance DATA_VOLUME |
| Create volume snapshot | openstack volume snapshot create --volume VOLUME_NAME_OR_ID --force SNAPSHOT_NAME|
| __Manage volumes after login into the instance__ | |
|  List storage devices  | fdisk -l |
|  Make filesystem on volume  | mkfs.ext4 /dev/vdb |
|  Create a mountpoint  | mkdir /data |
|  Config fstab (auto mount volume everytime vm start) & mount the volume at the mountpoint | cat << EOF >> /etc/fstab<br>/dev/vdb /data               ext4    defaults 0       0<br>EOF<br><br>mount -a|
|  Create a file on the volume  | touch /data/helloworld.txt<br>ls /data |
|  Unmount the volume  | _Unmount_:<br>umount /data<br><br>_Force execute unmount:_<br>umount -l /data |
|__Force remove volume stucked in the status "deleting"/"creating"/etc.__|WIP|