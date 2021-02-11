#!/usr/bin/env python3

import sys
import Crypto.Cipher
import Crypto.Util
import requests

site="http://crypto-class.appspot.com/po"
input_hex="f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
block_size = 16

def xor(a, b): return(Crypto.Util.strxor.strxor(bytearray([a]), bytearray([b]))[0])

def decrypt_block(ct_blocks, pt_block):
    block_num = len(ct_blocks)-1
    ct_block = ct_blocks[block_num-1]
    for pad_count in range(1, len(ct_block)+1):
        byte_idx = len(ct_block) - pad_count
        if pt_block[byte_idx] >= 0:
            # Aleady know this plaintext byte!
            print("pt: '"+"".join(map(lambda x: (chr(x) if x>16 else ("*" if x>0 else "_")), pt_block))+"'")
            continue
        padded_block = ct_block.copy()
        for pad_idx in range(byte_idx, len(padded_block)):
            padded_block[pad_idx] = xor(xor(ct_block[pad_idx], pad_count), pt_block[pad_idx] if pt_block[pad_idx] >= 0 else 0)
        found = False
        for guess in range(0, 256):
            block_under_test = padded_block.copy()
            block_under_test[byte_idx] = guess
            ct_blocks_copy = ct_blocks.copy()
            ct_blocks_copy[block_num-1] = block_under_test
            b_ary = b''.join(ct_blocks_copy)
            params={ 'er': b_ary.hex() }
            pt = xor(xor(guess, ct_blocks[block_num-1][byte_idx]), pad_count)
            r = requests.get(url=site, params=params)
            if r.status_code == 404:
                pt_block[byte_idx] = pt
                print("Found correct: guess="+hex(guess)+" ct_char="+hex(ct_blocks[block_num-1][byte_idx])+" pad="+hex(pad_count))
                found = True
                break
        if not found:
            print("\nError decrypting at block_num="+str(block_num)+" byte index="+str(byte_idx)+" pad_count="+str(pad_count))
            print("ct_blocks[block_num-1][byte_idx]="+hex(ct_blocks[block_num-1][byte_idx]))
            sys.exit(1)
        print("pt: '"+"".join(map(lambda x: (chr(x) if x>16 else ("("+str(x)+")" if x>0 else "_")), pt_block))+"'")
    
ct_blocks = []
pt_blocks = []
input_bytes = bytearray.fromhex(input_hex)
for i in range(0, int(len(input_bytes)/block_size)):
    ct_block = input_bytes[slice(i*block_size, (i+1)*block_size)]
    ct_blocks.append(ct_block)
    pt_blocks.append([-1]*len(ct_block))

# To input previously discovered plaintext, enter into pt_blocks here:
# pt_blocks[3][15] = 9

for block_num in range(len(ct_blocks)-1, 0, -1):
    decrypt_block(ct_blocks[slice(0, block_num+1)], pt_blocks[block_num])
print("'", end="")
for pt_block in pt_blocks:
    print("".join(map(lambda x: (chr(x) if x>16 else ("*" if x>0 else "_")), pt_block)), end="")
print("'")

sys.exit(0)
