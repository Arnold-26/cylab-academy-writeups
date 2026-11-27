import sys
raw = bytes.fromhex("2800000077677a627666626f6b747a6b7a7479687a696e7172766e666e7a6b726e756b6d657264676f6d6f6a0016100d1e0d09030220 1b161148131a3b0d09180814551a05335a0d5d48413813444703470845401b00".replace(" ", ""))
print("len", len(raw))
S = raw[4:44].decode()
B = raw[44:]
print("S =", S, len(S))
print("B =", B.hex(), len(B))

def show(tag, s):
    print("%-28s %s" % (tag, s))

# 1) Caesar
for k in range(26):
    t = "".join(chr((ord(c) - 97 + k) % 26 + 97) for c in S)
    if any(w in t for w in ("academy", "pico", "flag", "the", "sice")):
        show("caesar+%d" % k, t)
# 2) XOR lettres ^ blob (tronque)
t = bytes(a ^ b for a, b in zip(S.encode(), B)).decode("latin-1")
show("S xor B", t)
# 3) XOR avec blob decale de 1
t = bytes(a ^ b for a, b in zip(S.encode(), B[1:])).decode("latin-1")
show("S xor B[1:]", t)
# 4) rolling caesar : p[i] = c[i] - c[i-1]
t = "".join(chr((ord(S[i]) - ord(S[i-1])) % 26 + 97) for i in range(1, len(S)))
show("rolling diff", t)
t = "".join(chr((ord(S[i]) - ord(S[i-1])) % 26 + 97) for i in range(1, len(S)))
# 5) p[i] = c[i] - i
t = "".join(chr((ord(c) - i) % 26 + 97) for i, c in enumerate(S))
show("c - i", t)
# 6) p[i] = c[i] + i
t = "".join(chr((ord(c) + i) % 26 + 97) for i, c in enumerate(S))
show("c + i", t)
# 7) blob as ascii ?
show("B ascii", "".join(chr(x) if 32 <= x < 127 else "." for x in B))
# 8) XOR blob with 0x55 / keys
for k in (0x55, 0x41, 0x20, 0x13, 0x16, 0x28):
    show("B xor %#x" % k, "".join(chr(x ^ k) if 32 <= (x ^ k) < 127 else "." for x in B))
