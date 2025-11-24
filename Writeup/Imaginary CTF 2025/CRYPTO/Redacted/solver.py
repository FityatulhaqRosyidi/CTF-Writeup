
import itertools
result = bytes.fromhex("656cce6bc175617e5366c952d86c6a536e6ede52df636d7e757fce64d56373")

print(result, len(result))

# key nya didapat dari try and error
key = [
    ord('i') ^ 0x65,
    ord('c') ^ 0x6c,
    ord('t') ^ 0xce,
    ord('f') ^ 0x6b,
    ord('{') ^ 0xc1,
    ord('n') ^ 0x63,
    ord('}') ^ 0x73,
    ord('r') ^ 0x7e,
]

# untuk cek panjang key
# for length in range(2, 16):
#     good = True
#     for i, (r, k) in enumerate(zip(result, itertools.cycle(key))):
#         if i % len(key) <= 1:
#             if (r ^ k) < 0x20 or (r ^ k) > 0x7f:
#                 good = False
#     if good:
#         print(length)
#     key.append(0)

output = b""
for (r, k) in zip(result, itertools.cycle(key)):
    output += bytes([r ^ k])
print(output.decode())
                
