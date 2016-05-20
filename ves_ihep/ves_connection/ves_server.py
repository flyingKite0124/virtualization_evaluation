#!/usr/bin/env python
# coding=utf-8

import daemon
import fcntl
import socket
import hashlib
import os
import time
import json
import threading
from concurrent import futures


class ves_server(daemon.Daemon):

    def __init__(self, pidfile):
        daemon.Daemon.__init__(
            self,
            pidfile,
            stdout="/var/log/ves_server.log",
            stderr="/var/log/ves_server_err.log")
        self.threadpool = futures.ThreadPoolExecutor(max_workers=30)
        self.runningHost = list()
        self.runningPort = list()
        self.lock = threading.Lock()

    def _run(self):
        while True:
            with open("/ves_server/tasks") as fp:
                fcntl.flock(fp, fcntl.LOCK_EX)
                while len(self.runningHost) < 30:
                    line = fp.readline()
                    if not line:
                        break
                    activity = json.loads(line)
                    if self.lock.acquire():
                        if activity["ip"] not in self.runningHost:
                            self.runningHost.append(activity["ip"])
                            port = self._get_free_port()
                            thd = self.threadpool.submit(
                                self._run_activity, activity, port)
                            thd.add_done_callback(self._callback)
                        self.lock.release()

                fcntl.flock(fp, fcntl.LOCK_UN)
            time.sleep(5)

    def _get_free_port(self):
        for i in range(5655, 5685):
            if i not in self.runningPort:
                self.runningPort.append(i)
                return i

    def _callback(self, thd):
        ip, port, activity_history_id = thd.result()
        with open("/ves_server/tasks", "r+") as fp:
            fcntl.flock(fp, fcntl.LOCK_EX)
            if self.lock.acquire():
                self.runningHost.remove(ip)
                self.runningPort.remove(port)
                self.lock.release()
            lines = fp.readlines()
            fp.seek(0)
            for line in lines:
                activity = json.loads(line)
                if activity["activity_history_id"] != activity_history_id:
                    fp.write(line)
            fp.truncate()
            fcntl.flock(fp, fcntl.LOCK_UN)

    def _run_activity(self, activity, port):
        signal = threading.Event()
        signal.clear()
        header = dict()
        header["script_name"] = activity["script_name"]
        header["port"] = port
        header["filesize"] = os.path.getsize(activity["script_path"])
        jobIdGen = hashlib.md5()
        jobIdGen.update(
            str(activity["activity_history_id"]) + str(time.time()))
        header["jobId"] = jobIdGen.hexdigest()
        header["request"] = "new"
        header_new = json.dumps(header)
        header["request"] = "poll"
        header_poll = json.dumps(header)
        header["request"] = "kill"
        header_kill = json.dumps(header)
        child = Listen_sendback(activity, header["jobId"], port, signal)
        child.start()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((activity["ip"], 5555))
            sock.send("ves session start")
            success_info = sock.recv(1024)
            if success_info == "success":
                sock.send(header_kill)
                sock.recv(1024)
            sock.close()
            while True:
                if signal.is_set() == True:
                    break
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((activity["ip"], 5555))
                sock.send("ves session start")
                success_info = sock.recv(1024)
                if success_info == "success":
                    sock.send(header_new)
                    header_info = sock.recv(1024)
                    with open(activity["script_path"]) as fp:
                        while True:
                            filedata = fp.read(1024)
                            if not filedata:
                                break
                            sock.send(filedata)
                    sock.close()
                while True:
                    if signal.is_set() == True or signal.wait(5) == True:
                        break
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((activity["ip"], 5555))
                    sock.send("ves session start")
                    success_info = sock.recv(1024)
                    if success_info == "success":
                        sock.send(header_poll)
                        if sock.recv(1024) == "False":
                            sock.close()
                            break
                    sock.close()
            return activity["ip"], port, activity["activity_history_id"]
        except Exception as e:
            print(e)
            with open(activity["stdout_path"], "w") as fp:
                fp.write("host connected failed")
            with open(activity["stdout_path"], "w") as fp:
                fp.write("host connected failed")
            return activity["ip"], port, activity["activity_history_id"]


class Listen_sendback(threading.Thread):

    def __init__(self, activity, jobId, port, signal):
        threading.Thread.__init__(self)
        self.stdout_path = activity["stdout_path"]
        self.stderr_path = activity["stderr_path"]
        self.jobId = jobId
        self.port = port
        self.signal = signal

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", self.port))
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            start_session = conn.recv(1024)
            if start_session != "ves result session start":
                conn.close()
                continue
            else:
                conn.send("success")
            header_json = conn.recv(1024)
            header = json.loads(header_json)
            if header["jobId"] == self.jobId:
                if header["stdout_length"] != 0:
                    conn.send("receive stdout")
                    restsize = header["stdout_length"]
                    with open(self.stdout_path, "w") as fp:
                        while True:
                            if restsize > 1024:
                                filedata = conn.recv(1024)
                            else:
                                filedata = conn.recv(restsize)
                            if not filedata:
                                break
                            fp.write(filedata)
                            restsize = restsize - len(filedata)
                            if restsize <= 0:
                                break
                else:
                    open(self.stdout_path, "w").close()
                if header["stderr_length"] != 0:
                    conn.send("receive stderr")
                    restsize = header["stderr_length"]
                    with open(self.stderr_path, "w") as fp:
                        while True:
                            if restsize > 1024:
                                filedata = conn.recv(1024)
                            else:
                                filedata = conn.recv(restsize)
                            if not filedata:
                                break
                            fp.write(filedata)
                            restsize = restsize - len(filedata)
                            if restsize <= 0:
                                break
                else:
                    open(self.stderr_path, "w").close()
                conn.close()
                break
            else:
                conn.close()
        self.terminate_parent()

    def terminate_parent(self):
        self.signal.set()

if __name__ == "__main__":
    server = ves_server("/var/run/ves_server.pid")
    server.start()
