import pexpect
import getpass
import os
import traceback


def ssh_command(user, host, password, command):
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password:'])
    if i == 0:
        print 'Error'
        print 'SSH could ont login, Here is what SSH said:'
        print child.before, child.after
        return None
    if i == 1:
        child.senline('yes')
        child.expect([pexpect.TIMEOUT, 'password:'])
        if i == 0:
            print 'Error'
            print 'SSH could ont login, Here is what SSH said:'
            print child.before, child.after
            return None
        child.sendline(password)
        return child


def main():
    host = raw_input('Hostname: ')
    user = raw_input('User: ')
    password = getpass.getpass()
    command = raw_input('Enter the command: ')
    child = ssh_command(user, host, password, command)
    child.expect(pexpect.EOF)
    print child.before

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print str(e)
        traceback.print_exc()
        os._exit(1)
