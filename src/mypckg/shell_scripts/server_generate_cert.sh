#!/bin/bash
cd /etc/openvpn/easy-rsa
sudo su
source ./vars
ID=TESTE01
./build-key rasp$ID
# COMPRESS AND MOVE TO KEYS FOLDER TO DOWNLOAD
cd keys
tar -czvf /home/pribeiro/rasp$ID.tar rasp$ID.* ca.crt client.conf
