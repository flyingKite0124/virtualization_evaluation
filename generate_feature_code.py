#!/usr/bin/env python
#coding=utf-8
import uuid,socket,datetime,hashlib,os

def myMAC():
    mac=uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def myHostName():
    return socket.getfqdn(socket.gethostname())

def nowTime():
    return datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

def featureString():
    return myMAC()+myHostName()+nowTime()

def featureCode():
    m2=hashlib.md5()
    m2.update(featureString())
    return m2.hexdigest()

if __name__ == '__main__':
    feature_path=os.path.join(os.path.dirname(__file__),"ves_ihep","ves_connection","FEATURE_CODE")
    if not os.path.exists(feature_path):
        with open(feature_path,"w") as fp:
            fp.write(featureCode())
    os.chmod(feature_path,0o444)
