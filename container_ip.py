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
    print container_ip
    return container_ip
        