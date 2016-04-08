#!/usr/bin/env python

import socket
import sys


def socket_send(ip, script):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 1000))
    sock.send(script)
    result = ''
    while True:
        data = sock.recv(2048)
        if not data:
            sock.close()
            break
        else:
            result += data
    if result[-1] == '\n':
        result = result[:-1]
    return result
