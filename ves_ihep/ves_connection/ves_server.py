#!/usr/bin/env python
# coding=utf-8

import daemon
import fcntl
import time
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

    def _run(self):
        while True:
            with open("/ves_server/tasks") as fp:
                fcntl.flock(fp,fcntl.LOCK_EX)

                fcntl.flock(fp,fcntl.LOCK_UN)
            time.sleep(3)


if __name__ == "__main__":
    server = ves_server("/var/run/ves_server.pid")
    server.start()
