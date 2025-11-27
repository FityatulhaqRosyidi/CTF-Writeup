# solver 

# literally looping 1024 kali untuk ngambil key_m doang diakhir
# dapet key_m -> generate key aes -> decrypt flag


import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
from pwn import remote


# decode 
def decode_aes(ct, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    pt = aes.decrypt(ct)
    return unpad(pt, 16).decode()

r = remote("0.0.0.0", 5000)

params = json.loads(r.recvline())
n = params['n']
c = params['c']
iv = bytes.fromhex(params['iv'])
ct = bytes.fromhex(params['ct'])

for i in range(1024):
    r.recvline()
    r.sendline(b"1")
    r.recvline()
    print(f"Sent request {i+1}/1024")
    
key_m = json.loads(r.recvline())['key_m']
key = sha256(str(key_m).encode()).digest()[:16]
    
flag = decode_aes(ct, key, iv)

print("Flag:", flag)