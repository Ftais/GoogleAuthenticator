#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac, base64, struct, hashlib
import os, time
import json

def get_google_secret_code(secret):
    intervals_no = int(time.time()) // 30
    lens = len(secret)
    lenx = 8 - (8 if lens % 8 == 0 else lens % 8)
    secret += lenx * '='
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    # o = ord(h[19]) & 15 # used python 2
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    code = str(h).zfill(6)
    return code


# 持续获取google二次认证码
def continued_print_google_code(secret):
    while True:
        google_code = get_google_secret_code(secret)
        google_code_time = 30 - time.gmtime(time.time()).tm_sec % 30
        print("google_code : %s  (有效时间：%d 秒)" % (google_code, google_code_time))
        while True:
            if google_code == get_google_secret_code(secret):
                if time.gmtime(time.time()).tm_sec % 30 > 25:
                    print("google_code 马上失效 ,倒计时 %d s" % (30 - time.gmtime(time.time()).tm_sec % 30))
                    time.sleep(1)
                else:
                    time.sleep(2)
            else:
                break

def config_file_read(file_path):
    json_file = os.path.join(os.path.dirname(__file__),file_path)
    with open(json_file,"r") as f:
        json_f2a = json.loads(f.read())
        f.close
    return json_f2a


def run_demo1():
    print(get_google_secret_code(secret="BQ6KK6M5SUB44IJ5"))

def run_demo2():
    bybit_f2a = config_file_read('secret_code.json')
    continued_print_google_code(bybit_f2a['test']['s'])  

if __name__ == '__main__':
    run_demo1()
    run_demo2()
