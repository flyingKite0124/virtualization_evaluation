#!/usr/bin/env python
# coding=utf-8

import subprocess
import daemon
import threading
import socket
import os
import json


class ves_client(daemon.Daemon):

    def __init__(self, pidfile):
        daemon.Daemon.__init__(
            self,
            pidfile,
            stdout="/var/log/ves_client.log",
            stderr="/var/log/ves_client_err.log")

    def _run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 5555))
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            start_session = conn.recv(1024)
            if start_session != "ves session start":
                conn.send("fail")
                conn.close()
                continue
            else:
                conn.send("success")
            header_json = conn.recv(1024)
            header = json.loads(header_json)
            if header["request"] == "new":
                if threading.activeCount() == 1:
                    script_path = os.path.join(
                        "/ves/script", header["script_name"])
                    with open(script_path, "w") as fp:
                        restsize = header["filesize"]
                        while True:
                            if restsize > 1024:
                                filedata = conn.recv(1024)
                            else:
                                filedata = conn.recv(restsize)
                            if not filedata:
                                conn.close()
                                continue
                            fp.write(filedata)
                            restsize = restsize - len(filedata)
                            if restsize <= 0:
                                break
                    os.chmod(script_path, 0o755)
                    self.child_thread = Run_script_thread(
                        script_path, header["jobId"], (addr[0], header["port"]))
                    self.child_thread.start()
                else:
                    conn.close()
            elif header["request"] == "poll":
                if threading.activeCount() == 1:
                    conn.send("False")
                    conn.close()
                else:
                    jobId = self.child_thread.poll()
                    if jobId == header["jobId"]:
                        conn.send("True")
                    else:
                        conn.send("False")
                    conn.close()
            elif header["request"] == "kill":
                if threading.activeCount() != 1:
                    self.child_thread.terminate()
                conn.send("True")
                conn.close()
            else:
                conn.close()


class Run_script_thread(threading.Thread):

    def __init__(self, script_path, jobId, backsock):
        threading.Thread.__init__(self)
        self.script_path = script_path
        self.stage = "init"
        self.stop_flag = 0
        self.jobId = jobId
        self.backsock = backsock

    def run(self):
        self.stage = "start"
        self.child = subprocess.Popen(
            self.script_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        self.stage = "child_run"
        output = self.child.communicate()
        if self.stop_flag == 0:
            self.stage = "send_back"
            self.send_back(output)

    def terminate(self):
        self.stop_flag = 1
        if self.stage == "child_run":
            self.child.kill()

    def poll(self):
        return self.jobId

    def send_back(self, output):
        pass


class VesClientException(Exception):
    pass

if __name__ == "__main__":
    client = ves_client("/var/run/ves_client.pid")
    client.start()
