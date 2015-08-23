#install LXC
apt-get -y install lxc 

#create container
lxc-create -n allspark -t ubuntu 


#change SSH port
sed -i '/Port 22/c\Port 33968' /etc/ssh/sshd_config

#set logging
echo 'PROMPT_COMMAND='\'history -a '>(tee -a ~/.bash_history | logger -t " attacker_cmd  $USER[$$] $SSH_CONNECTION")'''\' >>/var/lib/lxc/base/rootfs/etc/bash.bashrc


