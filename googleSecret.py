#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac, base64, struct, hashlib, time


def get_google_secret_code(secret):
    intervals_no = int(time.time())//30
    lens = len(secret)
    lenx = 8 - (8 if lens % 8 == 0 else lens % 8)
    secret += lenx * '='
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    # o = ord(h[19]) & 15 # used python 2
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    code = str(h).zfill(6)
    return code


def continued_print_google_code(secret):
    while True:
        google_code = get_google_secret_code(secret)
        print("google_code : %s" % google_code)
        while True:
            if google_code == get_google_secret_code(secret):
                if time.gmtime(time.time()).tm_sec % 30 > 25:
                    print("google code will be invalid ,countdown %d s" % (30 - time.gmtime(time.time()).tm_sec % 30))
                    time.sleep(1)
                else:
                    time.sleep(2)
            else:
                break


if __name__ == '__main__':
    continued_print_google_code(secret="BQ6KK6M5SUB44IJ5")