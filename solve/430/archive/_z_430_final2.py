data = open("/tmp/winadb/config.bin", "rb").read()
size = int.from_bytes(data[:4], "little")
buf = bytearray(data[4:])
letters = bytes(buf[0:size])
blob = bytes(buf[size + 1:size + 1 + size])
print("FLAG_SIZE =", size, "| lettres:", letters.decode())
print("blob:", blob.hex())

def s8(x):
    x &= 0xff
    return x - 256 if x > 127 else x

def cmod(a, b):
    r = abs(a) % abs(b)
    return -r if a < 0 else r

def popcount(x):
    t = (x & 0x55) + ((x >> 1) & 0x55)
    u = (t & 0x33) + ((t >> 2) & 0x33)
    return (u & 0x0F) + ((u >> 4) & 0x0F)

def mutate(s, n):
    b = bytearray(s)
    sz = len(b)
    ch = 0x61
    for _ in range(n):
        for j in range(sz):
            v = s8(s8(b[j] - ch) + popcount(j % 0xFF))
            ch = s8(ch + cmod(v, 26))
            b[j] = ch & 0xFF
    return b

for n in range(0, 6):
    key = mutate(letters, n)
    pt = bytes(a ^ b for a, b in zip(blob, key))
    print("n=%d key=%r" % (n, bytes(key)))
    print("    pt =%r" % pt)
    print("    pt.decode =", pt.decode("latin-1"))
