import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
blob = bytes.fromhex("c38f0e4cbb7cfb61b99dfc5a5bdf69d2fe1bedf4ed67f400e8dfff")
print("blob len:", len(blob))
inp = bytearray(27)
i = 0
j = 0
k = 0
stop = False
while k <= 22 and not stop:
    m = 0
    while m <= 7:
        if j == 0:
            j = 1
        mask_in = 1 << (7 - m)
        mask_blob = 1 << (7 - j)
        bit = 1 if (blob[k] & mask_blob) else 0
        if bit:
            inp[i] |= mask_in
        else:
            inp[i] &= ~mask_in
        j += 1
        if j == 8:
            j = 0
            i += 1
        if i == 27:
            stop = True
            break
        m += 1
    k += 1
print("i final:", i, "k final:", k)
print("octets:", inp.hex())
print("repr:", bytes(inp))
print("imprimable:", all(32 <= b < 127 for b in inp))
