import socket,asyncore
import time
import threading
import datetime
import os
from subprocess import Popen, PIPE
import subprocess


global container_ip
container_ip = 'random'


class forwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip,remoteport,backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip=remoteip
        self.remoteport=remoteport
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)


    def tijd(self):
        ts = time.time()	
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
        return st

# creates a container if the containers does not exist   
    def create_container(self, con_name):
        con_dir = '/var/lib/lxc/' + attacker	
        if not os.path.exists(con_dir):
            create_con='lxc-clone -s -o base -n '+ str(con_name)
            Popen(create_con, shell=True, stdout=PIPE).communicate()[0]

	
    def get_container_ip(self, con_name):
    	get_con="lxc-info -n " + str(con_name) + " | grep IP | cut -d\' \' -f2-"
        con_dir = '/var/lib/lxc/' + attacker
        p = Popen(get_con, shell=True, stdout=PIPE) 	
    	output= p.stdout.read()
        print output
    	container_ip = output.lstrip()
    	print 'gestript'
    	print container_ip
        self.remoteip=container_ip
        f = open(condir + '/delta0/etc/ip, 'a')
        print f

    def clean_log(self):
        log_file='/var/lib/lxc/' + attacker + '/delta0/home/root/.bash_history'
        empty_file= ''
        #f = open(log_file, 'w')
        #f.writelines(empty_file)

    def start_container(self, con_name):
        get_con_info="lxc-info -n " + str(con_name) + " | grep State | cut -d\' \' -f2-"
        p = Popen(get_con_info, shell=True, stdout=PIPE) 	
        output= p.stdout.read()
        output = output.lstrip()
        print 'gestript'
        print output
        if 'RUNNING' in output:
            print "niks te doen"
            self.get_container_ip(attacker)
        else:	
            cmd5='lxc-start -d -n ' + str(con_name)
            Popen(cmd5, shell=True, stdout=PIPE).communicate()[0]
            time.sleep(4)
        self.get_container_ip(attacker)
        time.sleep(1)

    def logging(self, st, addr):
        f = open('attacker.log', 'a')
        print >> f, st, 'new connection from', addr

	

    def handle_accept(self):
        conn, addr = self.accept()
        print 'connection'       
        global st
        global attacker
        attacker = addr[0]
        st = self.tijd()
        print st , attacker
        self.logging(st,addr[0]) # write to attacker.log
        self.create_container(addr[0]) # if conatiner does not exist create one
        time.sleep(1)
        self.start_container(addr[0]) #determine conatiner state and start if neccecerly
        sender(receiver(conn),self.remoteip,self.remoteport)

class receiver(asyncore.dispatcher):
    def __init__(self,conn):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer=''
        self.to_remote_buffer=''
        self.sender=None

    def handle_connect(self):
        pass

    def logging(self, st, tty):
        f = open('attacker.log', 'a')
        print >> f, st, 'TTY from', attacker, tty

    def bash_history(self):
        log_path='/var/lib/lxc/' + attacker + '/delta0/root/.bash_history'
        if not os.path.exists(log_path):
            print 'no log vailable'
        else:
            print log_path
            with open(log_path) as f:
	        for line in f:
	            print st, line
                self.logging(st, line)	

    def handle_read(self):
        read = self.recv(8096)
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        #print '%04i <--'%sent
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def stop_container(self, con_name):
        time.sleep(30)
        cmd='lxc-stop -n ' + con_name
        print cmd        
        Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
        print "container gestopt"

    def no_block(self):
        self.stop_container(self.addr[0])

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()
	    print st + "connection close"
	    self.bash_history()
	    t = threading.Thread(name='child procs', target=self.no_block)
     	    t.start()
	    print "wordt uitgevoerd"	
 
    
class sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr,remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver=receiver
        receiver.sender=self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(8096)
        #print '<-- %04i'%len(read)
        self.receiver.to_remote_buffer += read

    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        # print '--> %04i'%sent
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()



if __name__=='__main__':
    forwarder('172.31.22.3',22, container_ip ,22)
    asyncore.loop()
