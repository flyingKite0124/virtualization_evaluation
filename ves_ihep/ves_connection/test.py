#!/usr/bin/env python
#coding=utf-8

import os
import pexpect
import client

def scp_cmd(ip,port,user,passwd,filename):
	scp=pexpect.spawn('scp -P%s %s %s@%s:/ves_ihep_scripts/' % (port,filename,user,ip))
	try:
		index = scp.expect(['password:','continue connecting (yes/no)?'],timeout=5)
		if index == 0:
			print ("t1")
			scp.sendline(passwd)
		elif index == 1:
			print "t2"
			scp.sendline("yes")
			scp.expect('password:')
			scp.sendline(passwd)
		scp.expect(pexpect.EOF)
	except pexpect.TIMEOUT:
		print "TIMEOUT: scp " + filename
		scp.close()

def ssh_cmd(ip,port,user, passwd, cmd):
	ssh = pexpect.spawn('ssh %s@%s -p%s "%s"' % (user,ip,port, cmd))
	try:
		index = ssh.expect(['password:','continue connecting (yes/no)?'],timeout=2)
		if index == 0:
			ssh.sendline(passwd)
		elif index == 1:
			ssh.sendline("yes")
			ssh.expect('password:')
			ssh.sendline(passwd)
		i = ssh.expect(['try again', pexpect.EOF],timeout=2)
		if i == 0:
			ret = 0
		elif i == 1:
			ret = 1
	except pexpect.TIMEOUT:
		print "TIMEOUT:"+ cmd
		ssh.close()
		ret = 0
	return ret

def check_file(ip,port,user, passwd):
	ssh = pexpect.spawn('ssh %s@%s -p%s "%s"' % (user,ip,port, "ls / | grep ves_ihep_scripts"))
	r = ''
	try:
		index = ssh.expect(['password:','continue connecting (yes/no)?'],timeout=2)
		if index == 0:
			ssh.sendline(passwd)
		elif index == 1:
			ssh.sendline("yes")
			ssh.expect('password:')
			ssh.sendline(passwd)
	except pexpect.TIMEOUT:
		print "TIMEOUT"
		ssh.close()
	else:
		r = ssh.read().strip()
		print r
		ssh.close()
	if r == "ves_ihep_scripts":
		ret = 1
	else:
		ret =0
	return ret

def remote_run(ip,port,user,passwd,filepath):
	scp_cmd(ip,port,user,passwd,filepath)
	filename = os.path.basename(filepath)
	ssh_cmd(ip,port,user,passwd,"chmod 755 /ves_ihep_scripts/"+filename)
	result=client.socket_send(ip,filename)
	return result

if __name__ == "__main__":
    ip='10.214.144.182'
    user='root'
    port='22'
    passwd='#srv@309'
    #test add_host ps:ssh_cmd(ip,port,user,passwd,"/ves_ihep_scripts/server.py") must TIMEOUT
    ssh_cmd(ip,port,user,passwd,"mkdir /ves_ihep_scripts")
    scp_cmd(ip,port,user,passwd,"/home/lv/virtualization_evaluation/ves_ihep/ves_connection/server.py")
    ssh_cmd(ip,port,user,passwd,"chmod 755 /ves_ihep_scripts/server.py")
    ssh_cmd(ip,port,user,passwd,"/ves_ihep_scripts/server.py")
    #test remote_run
    print remote_run(ip,port,user,passwd,"/home/lv/virtualization_evaluation/scripts/date.txt")
    #print check_file(ip,port,user,passwd)
