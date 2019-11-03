#!/usr/bin/env python
# -*- coding:utf-8 -*-


import hmac, base64, struct, hashlib, time
import sys
sys.path.append('../')


def get_f2a_code(secret):
    intervals_no = int(time.time())//30
    lens = len(secret)
    lenx = 8 - (8 if lens % 8 == 0 else lens % 8)
    secret += lenx * '='
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    code = str(h).zfill(6)
    return code
