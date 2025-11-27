
# versi server dari chall untuk nyoba soal

import json
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secrets import randbelow, token_bytes
from hashlib import sha256
import socket

HOST = "0.0.0.0"
PORT = 5000

flag = "flag{example_flag_for_imaginary_ctf_2025}"

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
d = pow(e, -1, (p-1)*(q-1))

key_m = randbelow(n)
key_c = pow(key_m, e, n)

key = sha256(str(key_m).encode()).digest()[:16]
iv = token_bytes(16)
ct = AES.new(key, AES.MODE_CBC, IV=iv).encrypt(pad(flag.encode(), 16))


def get_bit(n, k):
    return (n >> k) % 2

def send(conn, obj):
    conn.sendall((json.dumps(obj) + "\n").encode())

def recv(conn):
    data = conn.recv(4096)
    if not data:
        return None
    return json.loads(data.decode())

with socket.socket() as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[+] Connection from {addr}")
        try :
            send(conn, {'n': n, 'c': key_c, 'iv': iv.hex(), 'ct': ct.hex()})


            for _ in range(1024):
                idx = randbelow(4)
                send(conn, {'idx': idx})
                try:
                    response = recv(conn)
                    if not response:
                        break
                    c = response['c'] % n
                    assert c != key_c
                    m = pow(c, d, n)
                    b = get_bit(m, idx)
                except :
                    b = 2
                send(conn, {'b': b})

            send(conn, {'key_m': key_m})
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()
            print(f"[-] Connection closed from {addr}")

