import os
import pexpect

def ssh_cmd(ip,port,user, passwd, cmd):
    ret = 1
    ssh = pexpect.spawn('ssh %s@%s -p%s' % (user,ip,port))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)  
        if i == 0 :  
            ssh.sendline(passwd)
        elif i == 1:  
            ssh.sendline('yes\n')  
            ssh.expect('password: ')  
            ssh.sendline(passwd)  
        i= ssh.expect(['try again.','Last login:'],timeout=5)
        if i==0:
            ret=0
        elif i==1:
            ssh.sendline(cmd)  
            ssh.sendline("exit")
            ssh.close()
            ret=1 
    except pexpect.EOF:
        ssh.close()
        ret = 1
    except pexpect.TIMEOUT:
        ssh.close()  
        ret = 1
    return ret

ssh_cmd("10.214.144.188",22,"root","#srv309","echo success")