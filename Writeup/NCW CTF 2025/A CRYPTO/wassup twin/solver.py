# how to run: sage solver.py
# i run this on ubuntu with sage and pycryptodome installed

from Crypto.Util.number import long_to_bytes
from sage.all import *

# params 
N = 92226959634395542727305870286691824099
e = 65537
c = 81028662439340068660785564873246389821

# cari p dan q
f = factor(N)
p, q = f[0][0], f[1][0]

assert p * q == N

print("Found factors:")
print(f"p = {p}")
print(f"q = {q}")

# cari m0 
phi = (p - 1) * (q - 1)
d = pow(e, -1, int(phi))
m0 = pow(c, d, N)

# brutefroce
prefix = b"NCW{"

P = int.from_bytes(prefix, "big")
B = 256 ** (23 - len(prefix))

lower = P * B
upper = (P + 1) * B

L = (lower - m0) // N 
U = (upper - m0) // N

print(f"Searching k in range [{L}, {U}] (size = {U-L+1})")

def report_progress(iternum, total):
    print(f'Progress: {"{:,}".format(iternum)}/{"{:,}".format(total)} ({iternum/total*100:.2f}%)')

for k in range(L, U):

    # progress report
    if (k - L) % 1000000 == 0:
        report_progress(k - L, U - L)

    m = m0 + k * N
    b = long_to_bytes(m)
    if all(32 <= x < 127 for x in b) and b.endswith(b"}"):
        print(f"flag: {b.decode()}")
        break


    
