# SECURITY ONION INSTALLATION GUIDE

## 1. From ISO

### 1.1 Environment
- Hypervisor/Environment: KVM/OpenStack
- KVM guest configuration:
  - 8 CPUs, 8GB RAM, 80 GB Disk (min: 40GB)
  - 2 NICs:
    + Management NIC
    + Public NIC
- Iso: https://download.securityonion.net/file/Security-Onion-16/securityonion-16.04.6.3.iso

### 1.2 Step-by-step instructions

- Create a KVM guest/OpenStack instance (boot from iso + attach a volume with 80 GB free capacity):

![setup](images/0.png)

- Boot VM from iso as below (go to live CD mode as below):

![setup](images/1.png)

![setup](images/2.png)

- Click "Install SecurityOnion 16.04", then install OS (follows instructions on screen):

![setup](images/3.png)

![setup](images/4.png)

![setup](images/5.png)

![setup](images/6.png)

![setup](images/7.png)

![setup](images/8.png)

![setup](images/9.png)

![setup](images/10.png)

![setup](images/11.png)

![setup](images/12.png)

![setup](images/13.png)

- In the first time login to Security Onion, open terminal and setup static IP addresses for VM:

![setup](images/13.1.png)

- Setup IP addresses as below:

```sh
cat << EOF >> /etc/network/interfaces

# Public NIC
auto ens3
iface ens3 inet static
address 125.212.203.154/28
gateway 125.212.203.158

# Management NIC
auto ens6
iface ens6 inet static
address 10.60.1.29/24
EOF

ifconfig ens3 0
ifconfig ens6 0
/etc/init.d/networking restart
```

- Setup Security Onion Apps:
  - On Desktop, click "Setup":

![setup](images/14.png)

  - Follow instructions to setup Security Onion Apps as below:

![setup](images/15.png)

![setup](images/16.png)

![setup](images/17.png)

![setup](images/18.png)

![setup](images/19.png)

  - Setup user/password to access Kibana/Squert/Sguil:

![setup](images/20.png)

![setup](images/21.png)

![setup](images/22.png)

![setup](images/23.png)

![setup](images/24.png)

![setup](images/25.png)

![setup](images/26.png)

- Check Security Onion Apps status:

```sh
sudo sostat
```

- Access Security Onion Apps on browser:

  - Cyber Chef: https://localhost/cyberchef/cyberchef.htm

  - Kibana: https://localhost/app/kibana

  - Squert: https://localhost/app/squert