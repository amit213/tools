#!/bin/sh
#!/bin/bash
#ss

#### this is prep work for running docker on fresh containers.

#install docker.

echo  "This script needs sudo access"

sudo apt-get update
sudo apt-get install apt-transport-https -y
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
sudo apt-get update
sudo apt-get install lxc-docker -y

echo "Docker installation done."
echo "Adding $USER to docker group"
sudo adduser $USER docker



