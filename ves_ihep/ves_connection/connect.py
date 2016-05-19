#!/usr/bin/env python
# coding=utf-8

import os
import paramiko
import socket
import json


class Host(object):
    def __init__(self, ip, user, passwd, port=22):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.port = port


    def init_host(self,hostid):
        sock = socket.socket()
        sock.settimeout(2)
        try:
            sock.connect((self.ip, self.port))
            ssh = paramiko.Transport(sock)
            ssh.connect(username=self.user, password=self.passwd)
            sftp = paramiko.SFTPClient.from_transport(ssh)
            if "ves" not in sftp.listdir("/"):
                sftp.mkdir("/ves",0o755)
                feature=dict()
                with open(self._self_join("FEATURE_CODE")) as fp:
                    feature["server"]=fp.read().strip()
                feature["client"]=hostid
                sftp.open("/ves/feature","w").write(json.dumps(feature))
                sftp.mkdir("/ves/scripts")
                sftp.put(self._self_join("daemon.py"),"/ves/daemon.py")
                sftp.put(self._self_join("ves_client.py"),"/ves/ves_client.py")
                sftp.put(self._self_join("ves_client"),"/etc/init.d/ves_client")
                sftp.chmod("/etc/init.d/ves_client",0o755)
                sftp.put(self._self_join("client_setup.sh"),"/ves/client_setup.sh")
                sftp.chmod("/ves/client_setup.sh",0o755)
                self._exec_cmd("/ves/client_setup.sh")
                return hostid
            else:
                with open(self._self_join("FEATURE_CODE")) as fp:
                    feature=fp.read().strip()
                client_feature=json.loads(sftp.open("/ves/feature").read())
                if feature==client_feature["server"]:
                    return client_feature["client"]
                else:
                    return -1
        except Exception as e:
            print(e)
            return -2

    def _self_join(self,localfile):
        return os.path.join(os.path.dirname(__file__),localfile)



    def start_client(self):
        self._exec_cmd("service ves_client start")


    def test_connection(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip, self.port, self.user, self.passwd, timeout=2)
            stdin, stdout, stderr = ssh.exec_command("echo hello", timeout=2)
            if stdout.read().strip() == "hello":
                return True
        except Exception as e:
            print(e)
        return False

    def _exec_cmd(self,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip, self.port, self.user, self.passwd, timeout=2)
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=2)
            return ''.join(stdout.readlines())
        except Exception as e:
            print(e)
        return 0

    def _send_script(self, local_filepath):
        sock = socket.socket()
        sock.settimeout(2)
        try:
            sock.connect((self.ip, self.port))
            ssh = paramiko.Transport(sock)
            ssh.connect(username=self.user, password=self.passwd)
            sftp = paramiko.SFTPClient.from_transport(ssh)
            remote = os.path.join(
                "/ves",
                os.path.basename(local_filepath))
            sftp.put(local_filepath, remote)
            sftp.chmod(remote, 0o755)
            return True
        except Exception as e:
            print(e)
        return False



class HostException(Exception):
    pass




if __name__ == "__main__":
    host = Host("127.0.0.1", "root", "xqclzj123",5122)
    print(host.init_host(23))

