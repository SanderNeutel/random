import socket,asyncore
import time
import threading
import datetime
import os
from subprocess import Popen, PIPE
import subprocess



global container_ip
container_ip = 'random'

class for_log(asyncore.dispatcher):
    def __init__(self,var, st, attacker):
        self.logging(var, st, attacker)
        
    def logging(self,var, st, attacker):
        if 'open' in var:
            print var
            print st, attacker
            f = open('attacker.log', 'a')
            print >> f, st, '- New connection from:', attacker
        else:
            f = open('attacker.log', 'a')
            print >> f, st, '- Connection closed from:', attacker
            return     


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
    def create_container(self, con_name, ip_count):
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
                          
                
                

    def get_container_ip(self, con_name):
    	get_con="lxc-info -n " + str(con_name) + " | grep IP | cut -d\' \' -f2-"
        p = Popen(get_con, shell=True, stdout=PIPE)
        output= p.stdout.read()
        container_ip = output.lstrip()
        print container_ip
        self.remoteip=container_ip
        #with open(log_path) as f:
        #   for line in f:
        #      print line        

    def clean_log(self):
        log_file='/var/lib/lxc/' + attacker + '/delta0/home/root/.bash_history'
        empty_file= ''
        #f = open(log_file, 'w')
        #f.writelines(empty_file)

    def start_container(self, container_name):
        get_con_info="lxc-info -n " + str(container_name) + " | grep State | cut -d\' \' -f2-"
        p = Popen(get_con_info, shell=True, stdout=PIPE) 	
        output= p.stdout.read()
        output = output.lstrip()
        print 'gestript'
        print output
        if 'RUNNING' in output:
            print "niks te doen"
            self.get_container_ip(container_name)
        else:	
            cmd5='lxc-start -d -n ' + str(container_name)
            Popen(cmd5, shell=True, stdout=PIPE).communicate()[0]
            time.sleep(3)
        self.get_container_ip(Conatiner_name)
        time.sleep(1)

    def stop_container(self, con_name):
        time.sleep(600)
        cmd='lxc-stop -n ' + con_name
        print cmd        
        Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
        print "container gestopt"

    def no_block(self):
        self.stop_container(attacker)

    def handle_accept(self):
        conn, addr = self.accept()
        print 'connection'       
        global st
        global attacker
        global ip_count
        attacker = addr[0]
        st = self.tijd()
        print st , attacker
        #self.logging(st,addr[0]) # write to attacker.log
        a = for_log('open', st, attacker)
        print 'time'
        container_name= time.strftime("%Y_%m_%d") + '_' + addr[0]
        print container_name        
        self.create_container(container_name, ip_count) # if conatiner does not exist create one
        ip_count = ip_count + 1
        if ip_count == 100:
            ip_count = 20
        time.sleep(2)
        self.start_container(container_name) #determine conatiner state and start if neccecerly
        t = threading.Thread(name='child procs', target=self.no_block)
       # t.start()
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
	            self.logging(st, line)	
                #print st, line

    def handle_read(self):
        read = self.recv(8096)
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def stop_container(self, con_name):
        time.sleep(10)
        cmd='lxc-stop -n ' + con_name
        print cmd        
        Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
        print "container gestopt"

    def no_block(self):
        self.stop_container(attacker)

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()
	    print st + "connection close"
        self.bash_history()
        self.no_block()
        a = for_log('close', st, attacker)
        
	
 
    
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
    global ip_count
    ip_count = 21
    forwarder('172.31.22.3',22, container_ip ,22)
    asyncore.loop()
