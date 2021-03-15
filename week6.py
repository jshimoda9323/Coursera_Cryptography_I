#!/usr/bin/env python3

import sys
from gmpy2 import mpz, iroot, isqrt, sub, c_div, t_div, f_div, t_mod, powmod, mul, invert, t_divmod

"""
Challenge 1.
"""
N = mpz('179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581')
(A, is_exact) = iroot(N, 2)
if not is_exact:
    A = A + 1
x = isqrt(A**2 - N)
p = A - x
q = A + x
if p * q != N:
    print("1: Fail check")
print("1:")
print(p.digits() if p < q else q.digits())

"""
Challenge 2.
"""
N = mpz('648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877')

def get_min_of_factors(A_guess, N):
    x = isqrt(A_guess**2 - N)
    p = A_guess - x
    q = A_guess + x
    if p * q == N:
        result = p if p < q else q
        print("2: ")
        print(result.digits())
        return(True)
    return(False)

A = isqrt(N) + 1
count = 0
while not get_min_of_factors(A, N):
    A = A + 1
    count += 1
    if count > 2**21:
        break
#print("2: iterations: "+str(count))

"""
Challenge 3.
"""
N = mpz('720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929')

(A, is_exact) = iroot(6*N, 2)
if not is_exact:
    A = A + 1
"""
A == (3p+2q)/2  will always end in .5 since p and q are primes, and therefore so will x
So when A is adjusted to the next integer, we need to compensate in x.
Recognize that:
p * q == N
3p * 2q == 6N
3p = A - (x + 0.5)
2q = A + (x - 0.5)
6N == (A - (x + 0.5))*(A + (x - 0.5))
therefore,
2x == sqrt(4*A**2 - 4*A + 1 - 24*N)
3p == A - (x + 0.5)
6p == 2A - 2x - 1
p == 6p / 6
2q == A + (x - 0.5)
4q == 2A + 2x - 1
q = 4q / 4
"""
t0 = 4*(A**2) - 4*A + 1 - 24*N
twox, is_exact = iroot(t0, 2)
if not is_exact:
    print("twox is not an integer!!!")
    sys.exit(1)
sixp = 2*A-twox-1
fourq = 2*A+twox-1
p = t_div(sixp, 6)
q = t_div(fourq, 4)

if (p * q) != N:
    print("3: Fail check")
print("3:")
print(p.digits() if p < q else q.digits())

"""
Challenge 4.
"""
N = mpz('179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581')
C = mpz('22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540')
enc_exp = mpz('65537')
(A, is_exact) = iroot(N, 2)
if not is_exact:
    A = A + 1
x = isqrt(A**2 - N)
p = A - x
q = A + x
if p * q != N:
    print("4: Fail check p * q != N")

phi_N = N - p - q + 1
dec_exp = invert(enc_exp, phi_N)
if t_mod(enc_exp * dec_exp, phi_N) != mpz(1):
    print("4: Fail check e*d != 1")
pkcs_pt = powmod(C, dec_exp, N)
#print("pkcs plaintext:")
#print(pkcs_pt.digits(16))
res_C = powmod(pkcs_pt, enc_exp, N)
if res_C != C:
    print("4: Fail check res_C != C")
pt_hex = pkcs_pt.digits(16).split("00")[1]
print("4:")
print("'"+bytes.fromhex(pt_hex).decode('utf-8')+"'")
sys.exit(0)

