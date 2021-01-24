#!/usr/bin/env python3
import sys
from Crypto.Cipher import AES
import Crypto.Util
import Crypto.Util.Padding

input_data = [
        {"mode" : "CBC", "keyhex" : "140b41b22a29beb4061bda66b6747e14", "enchex" : "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"},
        {"mode" : "CBC", "keyhex" : "140b41b22a29beb4061bda66b6747e14", "enchex" : "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"},
        {"mode" : "CTR", "keyhex" : "36f18357be4dbd77f050515c73fcf9f2", "enchex" : "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"},
        {"mode" : "CTR", "keyhex" : "36f18357be4dbd77f050515c73fcf9f2", "enchex" : "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"},
        ]

class AESCipher:
    def __init__(self, key):
        self.key = key

    def decrypt(self, ivraw, encraw, mode):
        cipher = AES.new(key=self.key, mode=AES.MODE_ECB)
        outraw = b''
        text_remaining = encraw
        if mode == 'CBC':
            fwdblk = ivraw
            while text_remaining:
                outblock = cipher.decrypt(text_remaining[0:16])
                outblock = Crypto.Util.strxor.strxor(outblock, fwdblk)
                if len(text_remaining) > AES.block_size:
                    outraw += outblock
                else:
                    outraw += Crypto.Util.Padding.unpad(outblock, AES.block_size, 'pkcs7')
                fwdblk, text_remaining = text_remaining[0:16], text_remaining[16:]
            return(outraw)
        elif mode == 'CTR':
            outblock = cipher.decrypt(encraw[0:16])
            ctr = ivraw
            while text_remaining:
                outblock = cipher.encrypt(ctr)
                minlen = len(text_remaining[0:16])
                outraw += Crypto.Util.strxor.strxor(outblock[0:minlen], text_remaining[0:minlen])
                ctr = (int.from_bytes(ctr, 'big') + 1).to_bytes(AES.block_size, 'big')
                text_remaining = text_remaining[16:]
            return(outraw)
        else:
            print("Error: Unknown mode!")
            sys.exit(1)

for q in input_data:
    c = bytes.fromhex(q['enchex'])
    q['ivraw'], q['encraw'] = c[0:16], c[16:]
    q['keyraw'] = bytes.fromhex(q['keyhex'])
    aesc = AESCipher(q['keyraw'])
    q['msgraw'] = aesc.decrypt(q['ivraw'], q['encraw'], q['mode'])
    if q['msgraw']:
        print("'"+q['msgraw'].decode('utf-8')+"'")

