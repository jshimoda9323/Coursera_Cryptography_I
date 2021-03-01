#!/usr/bin/env python3

import sys
from gmpy2 import mpz, divm, mul, f_mod, powmod, add

p = mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')
g = mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')
h = mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')
B = mpz(2**20)

left_side = {}

g_pow_x1 = mpz(1)
left_side[h.digits()] = 0
for x1 in range(1, 2**20+1):
    g_pow_x1 = f_mod(mul(g_pow_x1, g), p)
    left_side[divm(h, g_pow_x1, p).digits()] = x1

g_pow_B = powmod(g, B, p)
found_x0 = None
found_x1 = None
for x0 in range(0, 2**20+1):
    ck = powmod(g_pow_B, x0, p)
    if ck.digits() in left_side:
        found_x0 = x0
        found_x1 = left_side[ck.digits()]
        break
else:
    print("Error: did not find x0")
    sys.exit(1)

x = add(mul(found_x0, B), found_x1)
print(x.digits())
sys.exit(0)
