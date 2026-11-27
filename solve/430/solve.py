# 430 - WinAntiDbg0x200  (Reverse Engineering, picoCTF 2024)
# Flag: academy{0x200_debug_f0r_Win_0d811b88}
# Write-up: ../../../writeups/reverse-engineering/430-winantidbg0x200.md
# Script exact utilise pour produire le flag.
#
import sys
data = open("/tmp/winadb/config.bin", "rb").read()
print("config:", data.hex(), "len", len(data))
size = int.from_bytes(data[:4], "little")
buf = bytearray(data[4:])
print("FLAG_SIZE =", size, " n(data) =", len(buf), " attendu 2*size+2 =", 2*size+2)
letters = bytes(buf[0:size])
blob = bytes(buf[size+1:size+1+size])      # FLAG = buf + FLAG_SIZE + 1
print("lettres:", letters)
print("blob   :", blob.hex())

def s8(x):
    x &= 0xff
    return x - 256 if x > 127 else x

def cmod(a, b):
    # C: reste du dividende
    r = abs(a) % abs(b)
    return -r if a < 0 else r

def mutate(s, n):
    b = bytearray(s)
    sz = len(b)
    ch = 0x61  # 'a'
    for it in range(n):
        for j in range(sz):
            t = ((j % 0xff) & 0x55) + (((j % 0xff) >> 1) & 0x55)
            u = (0x33 & t) + ((j // 0xff) & 0x33)
            v = s8(b[j] - ch) + (0x0f & u) + ((u >> 4) & 0x0f)
            v = s8(v)
            ch = s8(ch + cmod(v, 26))
            b[j] = ch & 0xff
    return b

best = []
for n in range(0, 400):
    key = mutate(letters, n)
    pt = bytes(a ^ b for a, b in zip(blob, key))
    try:
        s = pt.decode()
    except Exception:
        continue
    if all(32 <= c < 127 for c in pt):
        print("n=%3d -> %r" % (n, s))
        if "academy" in s or "pico" in s or "{" in s:
            print("  *** CANDIDAT ***")
            best.append((n, s))
print("candidats:", best)
