import socket,asyncore
import time
import threading
import datetime
import os
from subprocess import Popen, PIPE
import subprocess    
    
def getcontainer_ip(con_name):
    get_con="lxc-info -n " + str(con_name) + " | grep IP | cut -d\' \' -f2-"
    p = Popen(get_con, shell=True, stdout=PIPE)
    output= p.stdout.read()
    container_ip = output.lstrip()
    return container_ip
    
    
def create_container(con_name, ip_count):
    con_dir = '/var/lib/lxc/' + con_name	
    if not os.path.exists(con_dir):
        create_con='lxc-clone -s -o base -n '+ str(con_name)
        Popen(create_con, shell=True, stdout=PIPE).communicate()[0]
        log_path='/var/lib/lxc/' + con_name + '/config'
        print log_path
        c_ip= '10.0.3.' + str(ip_count)
        print c_ip
        cor_line = 'lxc.network.ipv4 = ' + c_ip + '/24'
        print cor_line      
        f = open(log_path,'a+')
        f.write(cor_line)
