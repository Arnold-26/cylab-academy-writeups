import struct

def try_size(path, label):
    raw = open(path, 'rb').read()
    size = struct.unpack('<I', raw[:4])[0]
    d = raw[4:]
    L = d[:size]
    CT = d[size+1:size+1+size]
    print(f"===== {label} size={size} =====")
    hits = []
    for n in range(0, 1024):
        flag = bytes(CT[j] ^ (97 + ((L[j] - 97 + n * bin(j % 255).count('1')) % 26)) for j in range(size))
        pr = sum(1 for c in flag if 32 <= c < 127)
        if flag.startswith(b'academy{') or flag.startswith(b'picoCTF{') or pr == size:
            hits.append((n, flag, pr))
    for n, flag, pr in hits:
        print(f"  n={n:4d} printable={pr}/{size} {flag}")

try_size('/tmp/w300/config.bin', '0x300')
try_size('/tmp/w200/config.bin', '0x200')
