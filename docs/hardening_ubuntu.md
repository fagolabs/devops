40 Linux Server Hardening Security Tips [2019 edition]

Securing your Linux server is important to protect your data, intellectual property, and time, from the hands of crackers (hackers). The system administrator is responsible for security of the Linux box. In this first part of a Linux server security series, I will provide 40 hardening tips for default installation of Linux system.

Linux Server Hardening Security Tips and Checklist
The following instructions assume that you are using CentOS/RHEL or Ubuntu/Debian based Linux distribution.

1. Encrypt Data Communication For Linux Server
All data transmitted over a network is open to monitoring. Encrypt transmitted data whenever possible with password or using keys / certificates.

Use scp, ssh, rsync, or sftp for file transfer. You can also mount remote server file system or your own home directory using special sshfs and fuse tools.
GnuPG allows to encrypt and sign your data and communication, features a versatile key management system as well as access modules for all kind of public key directories.
OpenVPN is a cost-effective, lightweight SSL VPN. Another option is to try out tinc that uses tunneling and encryption to create a secure private network between hosts on the Internet or private insecure LAN.
Lighttpd SSL (Secure Server Layer) Https Configuration And Installation
Apache SSL (Secure Server Layer) Https (mod_ssl) Configuration And Installation
How to configure Nginx with free Let’s Encrypt SSL certificate on Debian or Ubuntu Linux
2. Avoid Using FTP, Telnet, And Rlogin / Rsh Services on Linux
Under most network configurations, user names, passwords, FTP / telnet / rsh commands and transferred files can be captured by anyone on the same network using a packet sniffer. The common solution to this problem is to use either OpenSSH , SFTP, or FTPS (FTP over SSL), which adds SSL or TLS encryption to FTP. Type the following yum command to delete NIS, rsh and other outdated service:
# yum erase xinetd ypserv tftp-server telnet-server rsh-server

If you are using a Debian/Ubuntu Linux based server, try apt-get command/apt command to remove insecure services:
$ sudo apt-get --purge remove xinetd nis yp-tools tftpd atftpd tftpd-hpa telnetd rsh-server rsh-redone-server

3. Minimize Software to Minimize Vulnerability in Linux
Do you really need all sort of web services installed? Avoid installing unnecessary software to avoid vulnerabilities in software. Use the RPM package manager such as yum or apt-get and/or dpkg to review all installed set of software packages on a system. Delete all unwanted packages.
# yum list installed
# yum list packageName
# yum remove packageName

OR
# dpkg --list
# dpkg --info packageName
# apt-get remove packageName

4. One Network Service Per System or VM Instance
Run different network services on separate servers or VM instance. This limits the number of other services that can be compromised. For example, if an attacker able to successfully exploit a software such as Apache flow, he or she will get an access to entire server including other services such as MySQL/MariaDB/PGSql, e-mail server and so on. See how to install Virtualization software for more info:

Install and Setup XEN Virtualization Software on CentOS Linux 5
How To Setup OpenVZ under RHEL / CentOS Linux
5. Keep Linux Kernel and Software Up to Date
Applying security patches is an important part of maintaining Linux server. Linux provides all necessary tools to keep your system updated, and also allows for easy upgrades between versions. All security update should be reviewed and applied as soon as possible. Again, use the RPM package manager such as yum and/or apt-get and/or dpkg to apply all security updates.
# yum update

OR
# apt-get update && apt-get upgrade

You can configure Red hat / CentOS / Fedora Linux to send yum package update notification via email. Another option is to apply all security updates via a cron job. Under Debian / Ubuntu Linux you can use apticron to send security notifications. It is also possible to configure unattended upgrades for your Debian/Ubuntu Linux server using apt-get command/apt command:
$ sudo apt-get install unattended-upgrades apt-listchanges bsd-mailx

6. Use Linux Security Extensions
Linux comes with various security patches which can be used to guard against misconfigured or compromised programs. If possible use SELinux and other Linux security extensions to enforce limitations on network and other programs. For example, SELinux provides a variety of security policies for Linux kernel.

7. SELinux
I strongly recommend using SELinux which provides a flexible Mandatory Access Control (MAC). Under standard Linux Discretionary Access Control (DAC), an application or process running as a user (UID or SUID) has the user’s permissions to objects such as files, sockets, and other processes. Running a MAC kernel protects the system from malicious or flawed applications that can damage or destroy the system. See the official Redhat documentation which explains SELinux configuration.

8. Linux User Accounts and Strong Password Policy
Use the useradd / usermod commands to create and maintain user accounts. Make sure you have a good and strong password policy. For example, a good password includes at least 8 characters long and mixture of alphabets, number, special character, upper & lower alphabets etc. Most important pick a password you can remember. Use tools such as “John the ripper” to find out weak users passwords on your server. Configure pam_cracklib.so to enforce the password policy.

9. Set Up Password Aging For Linux Users For Better Security
The chage command changes the number of days between password changes and the date of the last password change. This information is used by the system to determine when a user must change his/her password. The /etc/login.defs file defines the site-specific configuration for the shadow password suite including password aging configuration. To disable password aging, enter:
# chage -M 99999 userName

To get password expiration information, enter:
# chage -l userName

Finally, you can also edit the /etc/shadow file in the following fields:

{userName}:{password}:{lastpasswdchanged}:{Minimum_days}:{Maximum_days}:{Warn}:{Inactive}:{Expire}:
Where,

Minimum_days: The minimum number of days required between password changes i.e. the number of days left before the user is allowed to change his/her password.
Maximum_days: The maximum number of days the password is valid (after that user is forced to change his/her password).
Warn : The number of days before password is to expire that user is warned that his/her password must be changed.
Expire : Days since Jan 1, 1970 that account is disabled i.e. an absolute date specifying when the login may no longer be used.
I recommend chage command instead of editing the /etc/shadow file by hand:
# chage -M 60 -m 7 -W 7 userName

Recommend readings:

Linux: Force Users To Change Their Passwords Upon First Login
Linux turn On / Off password expiration / aging
Lock the user password
Search for all account without password and lock them
Use Linux groups to enhance security
10. Restricting Use of Previous Passwords on Linux
You can prevent all users from using or reuse same old passwords under Linux. The pam_unix module parameter remember can be used to configure the number of previous passwords that cannot be reused.

11. Locking User Accounts After Login Failures
Under Linux you can use the faillog command to display faillog records or to set login failure limits. faillog formats the contents of the failure log from /var/log/faillog database / log file. It also can be used for maintains failure counters and limits.To see failed login attempts, enter:
faillog

To unlock an account after login failures, run:
faillog -r -u userName

Note you can use passwd command to lock and unlock accounts:
# lock account
passwd -l userName
# unlocak account
passwd -u userName

12. How Do I Verify No Accounts Have Empty Passwords?
Type the following command
# awk -F: '($2 == "") {print}' /etc/shadow

Lock all empty password accounts:
# passwd -l accountName

13. Make Sure No Non-Root Accounts Have UID Set To 0
Only root account have UID 0 with full permissions to access the system. Type the following command to display all accounts with UID set to 0:
# awk -F: '($3 == "0") {print}' /etc/passwd

You should only see one line as follows:

root:x:0:0:root:/root:/bin/bash
If you see other lines, delete them or make sure other accounts are authorized by you to use UID 0.

14. Disable root Login
Never ever login as root user. You should use sudo to execute root level commands as and when required. sudo does greatly enhances the security of the system without sharing root password with other users and admins. sudo provides simple auditing and tracking features too.

15. Physical Server Security
You must protect Linux servers physical console access. Configure the BIOS and disable the booting from external devices such as DVDs / CDs / USB pen. Set BIOS and grub boot loader password to protect these settings. All production boxes must be locked in IDCs (Internet Data Centers) and all persons must pass some sort of security checks before accessing your server. See also:

9 Tips To Protect Linux Servers Physical Console Access.
16. Disable Unwanted Linux Services
Disable all unnecessary services and daemons (services that runs in the background). You need to remove all unwanted services from the system start-up. Type the following command to list all services which are started at boot time in run level # 3:
# chkconfig --list | grep '3:on'

To disable service, enter:
# service serviceName stop
# chkconfig serviceName off

A note about systemd based Linux distro and services
Modern Linux distros with systemd use the systemctl command for the same purpose.

PRINT A LIST OF SERVICES THAT LISTS WHICH RUNLEVELS EACH IS CONFIGURED ON OR OFF
# systemctl list-unit-files --type=service
# systemctl list-dependencies graphical.target

TURN OFF SERVICE AT BOOT TIME
# systemctl disable service
# systemctl disable httpd.service

START/STOP/RESTART SERVICE
# systemctl disable service
# systemctl disable httpd.service

Get status of service
# systemctl status service
# systemctl status httpd.service

VIEWING LOG MESSAGES
# journalctl
# journalctl -u network.service
# journalctl -u ssh.service
# journalctl -f
# journalctl -k

17. Find Listening Network Ports
Use the following command to list all open ports and associated programs:
netstat -tulpn

OR use the ss command as follows:
$ ss -tulpn

OR
nmap -sT -O localhost
nmap -sT -O server.example.com

Top 32 Nmap Command Examples For Sys/Network Admins for more info. Use iptables to close open ports or stop all unwanted network services using above service and chkconfig commands.
update-rc.d like command on Redhat Enterprise / CentOS Linux.
Ubuntu / Debian Linux: Services Configuration Tool to Start / Stop System Services.
Get Detailed Information About Particular IP address Connections Using netstat Command.
18. Delete X Window Systems (X11)
X Window systems on server is not required. There is no reason to run X11 on your dedicated Linux based mail and Apache/Nginx web server. You can disable and remove X Windows to improve server security and performance. Edit /etc/inittab and set run level to 3. Finally, remove X Windows system, enter:
# yum groupremove "X Window System"

On CentOS 7/RHEL 7 server use the following commands:
# yum group remove "GNOME Desktop"
# yum group remove "KDE Plasma Workspaces"
# yum group remove "Server with GUI"
# yum group remove "MATE Desktop"

19. Configure Iptables and TCPWrappers based Firewall on Linux
Iptables is a user space application program that allows you to configure the firewall (Netfilter) provided by the Linux kernel. Use firewall to filter out traffic and allow only necessary traffic. Also use the TCPWrappers a host-based networking ACL system to filter network access to Internet. You can prevent many denial of service attacks with the help of Iptables:

How to setup a UFW firewall on Ubuntu 16.04 LTS server
How to set up a firewall using FirewallD on RHEL 8
Linux: 20 Iptables Examples For New SysAdmins
CentOS / Redhat Iptables Firewall Configuration Tutorial
Lighttpd Traffic Shaping: Throttle Connections Per Single IP (Rate Limit)
How to: Linux Iptables block common attack.
psad: Linux Detect And Block Port Scan Attacks In Real Time.
Use shorewall on CentOS/RHEL or Ubuntu/Debian Linux based server to secure your system.
20: Linux Kernel /etc/sysctl.conf Hardening
/etc/sysctl.conf file is used to configure kernel parameters at runtime. Linux reads and applies settings from /etc/sysctl.conf at boot time. Sample /etc/sysctl.conf:

# Turn on execshield
kernel.exec-shield=1
kernel.randomize_va_space=1
# Enable IP spoofing protection
net.ipv4.conf.all.rp_filter=1
# Disable IP source routing
net.ipv4.conf.all.accept_source_route=0
# Ignoring broadcasts request
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.icmp_ignore_bogus_error_messages=1
# Make sure spoofed packets get logged
net.ipv4.conf.all.log_martians = 1
21. Separate Disk Partitions For Linux System
Separation of the operating system files from user files may result into a better and secure system. Make sure the following filesystems are mounted on separate partitions:

/usr
/home
/var and /var/tmp
/tmp
Create separate partitions for Apache and FTP server roots. Edit /etc/fstab file and make sure you add the following configuration options:

noexec – Do not set execution of any binaries on this partition (prevents execution of binaries but allows scripts).
nodev – Do not allow character or special devices on this partition (prevents use of device files such as zero, sda etc).
nosuid – Do not set SUID/SGID access on this partition (prevent the setuid bit).
Sample /etc/fstab entry to to limit user access on /dev/sda5 (ftp server root directory):

/dev/sda5  /ftpdata          ext3    defaults,nosuid,nodev,noexec 1 2
22. Disk Quotas
Make sure disk quota is enabled for all users. To implement disk quotas, use the following steps:

Enable quotas per file system by modifying the /etc/fstab file.
Remount the file system(s).
Create the quota database files and generate the disk usage table.
Assign quota policies.
See implementing disk quotas tutorial for further details.
23. Turn Off IPv6 only if you are NOT using it on Linux
Internet Protocol version 6 (IPv6) provides a new Internet layer of the TCP/IP protocol suite that replaces Internet Protocol version 4 (IPv4) and provides many benefits. If you are NOT using IPv6 disable it:

RedHat / Centos Disable IPv6 Networking.
Debian / Ubuntu And Other Linux Distros Disable IPv6 Networking.
Linux IPv6 Howto – Chapter 19. Security.
Linux IPv6 Firewall configuration and scripts are and available here.
24. Disable Unwanted SUID and SGID Binaries
All SUID/SGID bits enabled file can be misused when the SUID/SGID executable has a security problem or bug. All local or remote user can use such file. It is a good idea to find all such files. Use the find command as follows:
#See all set user id files:
find / -perm +4000
# See all group id files
find / -perm +2000
# Or combine both in a single command
find / \( -perm -4000 -o -perm -2000 \) -print
find / -path -prune -o -type f -perm +6000 -ls

You need to investigate each reported file. See reported file man page for further details.

25: World-Writable Files on Linux Server
Anyone can modify world-writable file resulting into a security issue. Use the following command to find all world writable and sticky bits set files:
find /dir -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print

You need to investigate each reported file and either set correct user and group permission or remove it.

26. Noowner Files
Files not owned by any user or group can pose a security problem. Just find them with the following command which do not belong to a valid user and a valid group
find /dir -xdev \( -nouser -o -nogroup \) -print

You need to investigate each reported file and either assign it to an appropriate user and group or remove it.

27. Use A Centralized Authentication Service
Without a centralized authentication system, user auth data becomes inconsistent, which may lead into out-of-date credentials and forgotten accounts which should have been deleted in first place. A centralized authentication service allows you maintaining central control over Linux / UNIX account and authentication data. You can keep auth data synchronized between servers. Do not use the NIS service for centralized authentication. Use OpenLDAP for clients and servers.

28. Kerberos
Kerberos performs authentication as a trusted third party authentication service by using cryptographic shared secret under the assumption that packets traveling along the insecure network can be read, modified, and inserted. Kerberos builds on symmetric-key cryptography and requires a key distribution center. You can make remote login, remote copy, secure inter-system file copying and other high-risk tasks safer and more controllable using Kerberos. So, when users authenticate to network services using Kerberos, unauthorized users attempting to gather passwords by monitoring network traffic are effectively thwarted. See how to setup and use Kerberos.

29. Logging and Auditing
You need to configure logging and auditing to collect all hacking and cracking attempts. By default syslog stores data in /var/log/ directory. This is also useful to find out software misconfiguration which may open your system to various attacks. See the following logging related articles:

Linux log file locations.
How to send logs to a remote loghost.
How do I rotate log files?.
man pages syslogd, syslog.conf and logrotate.
30. Monitor Suspicious Log Messages With Logwatch / Logcheck
Read your logs using logwatch command (logcheck). These tools make your log reading life easier. You get detailed reporting on unusual items in syslog via email. A sample syslog report:

 ################### Logwatch 7.3 (03/24/06) ####################
        Processing Initiated: Fri Oct 30 04:02:03 2009
        Date Range Processed: yesterday
                              ( 2009-Oct-29 )
                              Period is day.
      Detail Level of Output: 0
              Type of Output: unformatted
           Logfiles for Host: www-52.nixcraft.net.in
  ##################################################################

 --------------------- Named Begin ------------------------

 **Unmatched Entries**
    general: info: zone XXXXXX.com/IN: Transfer started.: 3 Time(s)
    general: info: zone XXXXXX.com/IN: refresh: retry limit for master ttttttttttttttttttt#53 exceeded (source ::#0): 3 Time(s)
    general: info: zone XXXXXX.com/IN: Transfer started.: 4 Time(s)
    general: info: zone XXXXXX.com/IN: refresh: retry limit for master ttttttttttttttttttt#53 exceeded (source ::#0): 4 Time(s)

 ---------------------- Named End -------------------------

  --------------------- iptables firewall Begin ------------------------

 Logged 87 packets on interface eth0
   From 58.y.xxx.ww - 1 packet to tcp(8080)
   From 59.www.zzz.yyy - 1 packet to tcp(22)
   From 60.32.nnn.yyy - 2 packets to tcp(45633)
   From 222.xxx.ttt.zz - 5 packets to tcp(8000,8080,8800)

 ---------------------- iptables firewall End -------------------------

 --------------------- SSHD Begin ------------------------

 Users logging in through sshd:
    root:
       123.xxx.ttt.zzz: 6 times

 ---------------------- SSHD End -------------------------

 --------------------- Disk Space Begin ------------------------

 Filesystem            Size  Used Avail Use% Mounted on
 /dev/sda3             450G  185G  241G  44% /
 /dev/sda1              99M   35M   60M  37% /boot

 ---------------------- Disk Space End -------------------------

 ###################### Logwatch End #########################
See Common Linux log files names and usage for more info.

31. System Accounting with auditd
The auditd is provided for system auditing. It is responsible for writing audit records to the disk. During startup, the rules in /etc/audit.rules are read by this daemon. You can open /etc/audit.rules file and make changes such as setup audit file log location and other option. With auditd you can answers the following questions:

System startup and shutdown events (reboot / halt).
Date and time of the event.
User respoisble for the event (such as trying to access /path/to/topsecret.dat file).
Type of event (edit, access, delete, write, update file & commands).
Success or failure of the event.
Records events that Modify date and time.
Find out who made changes to modify the system’s network settings.
Record events that modify user/group information.
See who made changes to a file etc.
See our quick tutorial which explains enabling and using the auditd service.

32. Secure OpenSSH Server
The SSH protocol is recommended for remote login and remote file transfer. However, ssh is open to many attacks. See how to secure OpenSSH server:

Top 20 OpenSSH Server Best Security Practices.
Secure your Linux desktop and SSH login using two factor Google authenticator.
33. Install And Use Intrusion Detection System
A network intrusion detection system (NIDS) is an intrusion detection system that tries to detect malicious activity such as denial of service attacks, port scans or even attempts to crack into computers by monitoring network traffic.

It is a good practice to deploy any integrity checking software before system goes online in a production environment. If possible install AIDE software before the system is connected to any network. AIDE is a host-based intrusion detection system (HIDS) it can monitor and analyses the internals of a computing system. I recommended that you install and use rkhunter root kit detection software too.

34. Disable USB/firewire/thunderbolt devices
Type the following command to disable USB devices on Linux system:
# echo 'install usb-storage /bin/true' >> /etc/modprobe.d/disable-usb-storage.conf

You can use same method to disable firewire and thunderbolt modules:
# echo "blacklist firewire-core" >> /etc/modprobe.d/firewire.conf
# echo "blacklist thunderbolt" >> /etc/modprobe.d/thunderbolt.conf

Once done, users can not quickly copy sensitive data to USB devices or install malware/viruses or backdoor on your Linux based system.

35. Disable unused services
You can disable unused services using the service command/systemctl command:
$ sudo systemctl stop service
$ sudo systemctl disable service

For example, if you are not going to use Nginx service for some time disable it:
$ sudo systemctl stop nginx
$ sudo systemctl disable nginx

36. Use fail2ban/denyhost as IDS (Install an Intrusion Detection System)
Fail2ban or denyhost scans the log files for too many failed login attempts and blocks the IP address which is showing malicious signs. See how to install and use denyhost for Linux. One can install fail2ban easily:
$ sudo apt-get install fail2ban

OR
$ sudo yum install fail2ban

Edit the config file as per your needs:
$ sudo vi /etc/fail2ban/jail.conf

Restart the service:
$ sudo systemctl restart fail2ban.service

Debian / Ubuntu Linux Install Advanced Intrusion Detection Environment (AIDE) Software
psad: Linux Detect And Block Port Scan Attacks In Real Time
37. Secure Apache/PHP/Nginx server
Edit httpd.conf file and add the following:

ServerTokens Prod
ServerSignature Off
TraceEnable Off
Options all -Indexes
Header always unset X-Powered-By
Restart the httpd/apache2 server on Linux, run:
$ sudo systemctl restart apache2.service

OR
$ sudo systemctl restart httpd.service

You must install and enable mod_security on RHEL/CentOS server. It is recommended that you edit php.ini and secure it too.

Top 25 Nginx Web Server Best Security Practices
How to analyze Nginx configuration files for security misconfiguration on Linux or Unix
38. Protecting Files, Directories and Email
Linux offers excellent protections against unauthorized data access. File permissions and MAC prevent unauthorized access from accessing data. However, permissions set by the Linux are irrelevant if an attacker has physical access to a computer and can simply move the computer’s hard drive to another system to copy and analyze the sensitive data. You can easily protect files, and partitons under Linux using the following tools:

To encrypt and decrypt files with a password, use gpg command.
Linux or UNIX password protect files with openssl and other tools.
Full disk encryption is a must for securing data, and is supported by most Linux distributions. See how to encrypting harddisk using LUKS on Linux. Make sure swap is also encrypted. Require a password to edit bootloader.
Make sure root mail is forwarded to an account you check.
Howto: Disk and partition encryption in Linux for mobile devices.
Linux Securing Dovecot IMAPS / POP3S Server with SSL Configuration.
Linux Postfix SMTP (Mail Server) SSL Certificate Installations and Configuration.
Courier IMAP SSL Server Certificate Installtion and Configuration.
Configure Sendmail SSL encryption for sending and receiving email.
39. Backups
It cannot be stressed enough how important it is to make a backup of your Linux system. A proper offsite backup allows you to recover from cracked server i.e. an intrusion. The traditional UNIX backup programs are dump and restore are also recommended. You must set up encrypted backups to external storage such as NAS server or FreeNAS server or use cloud computing service such as AWS:

Debian / Ubuntu Linux Install and Configure Remote Filesystem Snapshot with rsnapshot Incremental Backup Utility
How To Set Red hat / CentOS Linux Remote Backup / Snapshot Server
How To Back Up a Web Server
How To Use rsync Command To Backup Directory Under Linux
40. Other Recommendation:
How to look for Rootkits on Linux based server.
How to Enable ExecShield Buffer Overflows Protection on Linux based server.
EUD Security Guidance: Ubuntu 16.04 LTS
A Guide For Securing RHEL 7
Basic and advanced config OF SELINUX
Subscribe to Redhat or Debian Linux security mailing list or RSS feed.


Refs
---
1. https://www.cyberciti.biz/tips/linux-security.html
2. https://www.lifewire.com/harden-ubuntu-server-security-4178243
