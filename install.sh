#install LXC
apt-get install -y lxc 

#create container
lxc-create -n allspark -t ubuntu 

#set logging
PROMPT_COMMAND='history -a >(tee -a ~/.bash_history | logger -t " attacker_cmd  $USER[$$] $SSH_CONNECTION")'

$change SSH port
sed -i '/Port 22/c\Port 33968' /etc/ssh/sshd_config

sed "/cdef/aline1\nline2\nline3\nline4" input.txt
