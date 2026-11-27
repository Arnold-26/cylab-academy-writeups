import struct

def cmod(a, m):
    r = abs(a) % m
    return -r if a < 0 else r

for p in ['/tmp/w300/config.bin', '/tmp/w200/config.bin']:
    raw = open(p, 'rb').read()
    size = struct.unpack('<I', raw[:4])[0]
    d = raw[4:]
    L = d[:size]
    CT = d[size+1:size+1+size]
    key = bytes((97 + cmod(L[j] - 97 + bin(j % 255).count('1'), 26)) & 0xFF for j in range(size))
    flag = bytes(CT[j] ^ key[j] for j in range(size))
    print(p, 'size', size)
    print('  key ', key)
    print('  flag', flag)
    print()
