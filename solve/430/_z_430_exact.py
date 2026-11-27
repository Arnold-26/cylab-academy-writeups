import struct, sys

def sbyte(x):
    x &= 0xFF
    return x - 256 if x >= 128 else x

def cmod(a, m):
    # C truncating modulo (idiv)
    r = abs(a) % m
    return -r if a < 0 else r

def run(path, n=1, verbose=True):
    raw = open(path, 'rb').read()
    size = struct.unpack('<I', raw[:4])[0]
    data = bytearray(raw[4:])
    if verbose:
        print(f"{path}: filesize={len(raw)} size={size} datalen={len(data)} (2*size+2={2*size+2})")
    assert len(data) == 2*size + 2, "taille incoherente"
    # ReadConfig: CONFIG_BUFFER = malloc(200), fread remplit `data`
    buf = bytearray(200)
    buf[0:len(data)] = data
    # FLAG = CONFIG_BUFFER + size + 1  (taille = size)
    FLAG_OFF = size + 1
    ch = sbyte(0x61)
    for _ in range(n):
        for j in range(size):
            m = j % 255
            T = (m & 0x55) + ((m >> 1) & 0x55)
            U = (T & 0x33) + ((T >> 2) & 0x33)
            pc = (U & 0x0F) + ((U >> 4) & 0x0F)
            v = buf[j] - ch + pc          # movzx buf[j] - movsx ch + pc
            ch = sbyte(ch + cmod(v, 26))
            buf[j] = ch & 0xFF
    flag = bytes(buf[FLAG_OFF + i] ^ buf[i] for i in range(size))
    if verbose:
        print(f"  cle muee = {bytes(buf[:size])!r}")
        print(f"  flag brut = {flag!r}")
    return flag

for p in sys.argv[1:] or ['/tmp/w300/config.bin']:
    for n in (1,):
        f = run(p, n)
        print(f"  -> n={n} {f.decode('utf-8', 'replace')}")
    print()
