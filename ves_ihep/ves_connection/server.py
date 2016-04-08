#!/usr/bin/env python

import socket
import os
import sys


def work():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ', Error message : ' + msg[1]
        sys.exit()
    print 'socket created!'
    try:
        sock.bind(('0.0.0.0', 1000))
    except socket.error as msg:
        print 'Bind Failed, Error code : ' + str(msg[0]) + 'Message ' + msg[1]
        sys.exit(1)
    print 'socket bind complete!'
    sock.listen(10)
    print 'socket now listening!'
    while True:
        try:
            conn, addr = sock.accept()
            print 'Got connection from', addr
            script_name = conn.recv(2048)
            r = os.popen('/ves_ihep_scripts/' + script_name).read()
            conn.send(r)
            conn.close()
        except KeyboardInterrupt:
            print("Now we will exit")
            sys.exit(0)
    sock.close()

if __name__ == "__main__":
    work()
