#!/usr/bin/env python
# coding=utf-8

import subprocess
import threading
import socket
import os
import json
import atexit


class ves_client(object):
    def __init__(self):
        atexit.register(self.kill_child)

    def kill_child(self):
        if threading.activeCount !=1:
            self.child_thread.terminate()
        else:
            print("no child")

    def run(self):
        print("")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 5555))
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            start_session = conn.recv(1024)
            if start_session != "ves session start":
                print(start_session)
                conn.send("fail")
                conn.close()
                continue
            else:
                conn.send("success")
            header_json = conn.recv(1024)
            header = json.loads(header_json)
            print(header["request"])
            if header["request"] == "new":
                if threading.activeCount() == 1:
                    print("new_success")
                    # script_path = os.path.join(
                    #     "/ves/script", header["script_name"])
                    script_path="./testreceive"
                    with open(script_path,"w") as fp:
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
                    print("new_failure")
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
        print("childrun")
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
        print("stdout:%s"%output[0])
        print("stderr:%s"%output[1])
        print("jobId:",self.jobId)
        print("backsock:",self.backsock)


class VesClientException(Exception):
    pass


if __name__ == "__main__":
    client = ves_client()
    client.run()
