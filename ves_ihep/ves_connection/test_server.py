#!/usr/bin/python
#coding=utf-8

import socket
import json
import os
import sys

header=dict()
header["request"]="new"
header["script_name"]="testscript"
header["jobId"]="1111"
header["port"]=5556
header["filesize"]=os.path.getsize(header["script_name"])
header_new=json.dumps(header)
header["request"]="poll"
header_poll=json.dumps(header)
header["request"]="kill"
header_kill=json.dumps(header)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.settimeout(1)

try:
    sock.connect(("127.0.0.1",5555))
    sock.send("ves session start")
    success_info=sock.recv(1024)
    if success_info=="success":
        if sys.argv[1]=="new":
            sock.send(header_new)
            with open(header["script_name"]) as fp:
                while True:
                    filedata=fp.read(1024)
                    if not filedata:
                        break
                    sock.send(filedata)
        elif sys.argv[1]=="poll":
            sock.send(header_poll)
            print(sock.recv(1024))
        elif sys.argv[1]=="kill":
            sock.send(header_kill)
            print(sock.recv(1024))
    else:
        print("connection failure")
    sock.close()

except Exception as e:
    print(e)

