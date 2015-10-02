#install LXC
apt-get -y install lxc 

#forwarding tor
iptables -A PREROUTING -i lxcbr0 -p tcp --syn -j REDIRECT --to-ports 9040
iptables -A PREROUTING -i lxcbr0 -p udp --dport 53 -j REDIRECT --to-ports 53

#create container
lxc-create -n allspark -t ubuntu 


#change SSH port
sed -i '/Port 22/c\Port 33968' /etc/ssh/sshd_config
service ssh restart

#set logging
echo 'PROMPT_COMMAND='\'history -a '>(tee -a ~/.bash_history | logger -t " attacker_cmd  $USER[$$] $SSH_CONNECTION")'''\' >>/var/lib/lxc/base/rootfs/etc/bash.bashrc


