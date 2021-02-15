#!/usr/bin/env python3

import sys
import requests

site="http://crypto-class.appspot.com/po"
input_hex="f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
bs = 16

def decrypt_block(ct):
    orig_ct = ct.copy()
    pt = bytearray(len(ct))
    for pad_count in range(1, bs+1):
        ct = orig_ct.copy()
        decrypt_idx = len(ct) - bs - pad_count
        for pad_index in range(decrypt_idx, len(ct)-bs):
            ct[pad_index] = orig_ct[pad_index] ^ pad_count ^ pt[pad_index]
        found = False
        for guess in range(128):
            ct[decrypt_idx] = orig_ct[decrypt_idx] ^ guess ^ pad_count
            params = { 'er' : ct.hex() }
            r = requests.get(url=site, params=params)
            if r.status_code == 404:
                pt[decrypt_idx] = guess
                print("Found: guess="+hex(guess))
                found = True
                break
        if not found:
            print("Assume guess="+str(pad_count))
            pt[decrypt_idx] = pad_count

input_bytes = bytearray.fromhex(input_hex)
for block_num in range(2, 5):
    pt = decrypt_block(input_bytes[0:bs*block_num].copy())
    print("pt: '"+"".join(map(lambda x: (chr(x) if x>16 else ("("+str(x)+")" if x>0 else "_")), pt))+"'")
