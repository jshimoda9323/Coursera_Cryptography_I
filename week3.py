#!/usr/bin/env python3
import sys
from Crypto.Hash import SHA256

if len(sys.argv) != 2:
    print("week3.py <file>", file=sys.stderr)
    sys.exit(1)
file_contents = []

with open(sys.argv[1], "rb") as input_file:
    while True:
        part = input_file.read(1024)
        if part:
            file_contents.append(part)
        else:
            break

file_contents.reverse()
h0 = SHA256.new()
prev = b''
for part in file_contents:
    part = part + prev
    h = h0.copy()
    h.update(part)
    prev = h.digest()
print(h.hexdigest())
sys.exit(0)

