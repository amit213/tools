#!/bin/sh
#!/bin/bash
#ss

#### this is prep work 

#cloud-config

sudo apt-get update -y;
#sudo apt-get install sl fail2ban iputils-ping curl ntpdate python3-pip vim libffi-dev libssl-dev open-vm-tools --fix-missing -y;
sudo apt-get install docker-compose jq -y;
sudo ntpdate -s time.nist.gov;
sudo timedatectl set-timezone America/Los_Angeles;
# - sudo sed -i "2i`hostname -I | awk '{print $1}'` `cat /etc/hostname`" /etc/hosts
#curl -fsSL get.docker.com | sh;
echo ""alias reloadenv=\''source /dev/stdin <<< "$(curl -s -L bit.ly/sh213)"'\'"" >> /home/vmuser/.bashrc
echo "disable_vmware_customization: false" >> /etc/cloud/cloud.cfg
echo "custom cloud config v0.501 `date`" >> /tmp/foopack.txt
vmtoolsd --cmd "info-get guestinfo.foo" >> /tmp/set-hostname.txt
sudo cat /tmp/set-hostname.txt > /etc/hostname
sudo sed -i "2i`hostname -I | awk '{print $1}'` `cat /etc/hostname`" /etc/hosts
