#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 2016-11-08 21:45:01

import socket
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
import struct
import time

# ***替换成学号
account = '***********'
# ***替换成学号
baccount = b'**********'
# 路由器 WAN口的MAC 地址 (ipconfig)  
mac = b"AA:BB:CC:DD:EE:FF"
# 你的密码
password = '******'

def pswd_encrypt(passwd, key):
    pe = ""
    for i in range(0, len(passwd)):
        ki = ord(passwd[i]) ^ ord(key[len(key) - i % len(key) - 1])
        _l = chr((ki & 0x0f) + 0x36)
        _h = chr((ki >> 4 & 0x0f) + 0x63)
        if(i % 2 == 0):		# reverse
            pe += _l + _h
        else:
            pe += _h + _l

    return pe

def usr_encrypt(username):
    res = ""
    for i in range(0, len(username)):
        res += chr(ord(username[i]) + 4)
    return res


def get_headers():
    return {
        "Content-Type" : "application/x-www-form-urlencoded",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "SRun-Version": "SRun3K Client_XW117S0B60119A-SRun3K.Portal",
        #"SRun-AuthorizationCRC32": "BD9852E5",
        "DiskDevice": "|",
        'OSName': 'Microsoft Professional (build 9200), 64-bit',
        #'SRun-ClientTime': '1456641787',
        'SRun-ClientGUID': '{F7891AFF-1031-E288-175D-BF1DA46688B7}',
        #'SRun-AuthorizationKey': 'a0445fa2c1f45b763c3547c4645a670c',
        "CPUDevice": '|',
        'OSVersion': '6.2 Build9200',
        #'SRun-AuthorizationCKey': 'FEF16E77DE959883454E02A6E4F058D2',
    }

def http_post(url, po_dict):
    req = Request(url, urlencode(po_dict).encode('utf-8'))
    try:
        with urlopen(req) as response:
            return response.read()
    except HTTPError as e:
        print("The server couldn't fulfill the request.")
    except URLError as e:
        print('Invalid url :', url)

def dropheart():
    pack = struct.pack('! 12s 20x 17s 7x', baccount, mac)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i = 0
    while True:
        s.sendto(pack, ('172.16.154.130', 3338))
        s.sendto(pack, ('172.16.154.130', 4338))
        i = i + 1
        print('Heartbeat', i)
        # 此处调整心跳包发送时间间隔，单位 second
        time.sleep(50)
        with open('/proc/net/arp', 'r') as fh:
                dh = fh.read()
        if dh.count("0x2") < 2:
            break
            print("OFFLINE")
        
def login():
    po_dict = {
        "action":"login",
        "username": "",
        "password":"",
        "drop": 0,
        "pop":1,
        "type":2,
        "n":117,
        "mbytes":0,
        "minutes":0,
        "ac_id":1,
    }

    po_dict["username"] = "{SRUN3}\r\n" + usr_encrypt(account)
    #print(po_dict['username'])
    po_dict["password"] = pswd_encrypt(password, '1234567890')
    rs = http_post("http://172.16.154.130:69/cgi-bin/srun_portal", po_dict) #'http://172.16.154.130/cgi-bin/rad_user_info', po_dict) #
    print(rs.decode('utf-8'))
    # print(po_dict['password'])

def main():
    print('Running...')
    lt = 0
    while True:
        lt = lt + 1
        print('Login:', lt) #登陆次数
        with open('/proc/net/arp', 'r') as f:
            d = f.read()
        print("Online User: ", d.count("0x2")-1)
        if d.count("0x2") >= 2:
            login()
            dropheart()
        time.sleep(15) #睡眠15后继续循环

if __name__ == '__main__':
    main()
