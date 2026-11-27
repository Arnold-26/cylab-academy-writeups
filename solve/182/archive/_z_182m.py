import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
stored = bytes.fromhex("7b7f780f0675153e0f1b694e0c0f78393d0a117e4d3d5810641050082a3a3b01102f16690710321f")
print("stored len:", len(stored), "hex:", stored.hex())


def step_xor(i):
    x = i % 10
    x ^= 9 if i % 2 == 0 else 8
    x ^= 7 if i % 3 == 0 else (6 if i % 3 == 1 else 5)
    return x


def forward(data, use_const20=True, use_prev=True, use_prev3=True):
    d = bytearray(data)
    for i in range(len(d)):
        if use_const20:
            d[i] ^= 20
        if use_prev and i > 0:
            d[i] ^= d[i - 1]
        if use_prev3 and i > 2:
            d[i] ^= d[i - 3]
        d[i] ^= step_xor(i)
    return bytes(d)


def backward(data):
    d = bytearray(data)
    for i in range(len(d)):
        v = d[i]
        v ^= step_xor(i)
        if i > 2:
            v ^= data[i - 3]
        if i > 0:
            v ^= data[i - 1]
        v ^= 20
        d[i] = v
    return bytes(d)


def show(label, b):
    asc = "".join(chr(c) if 32 <= c < 127 else "." for c in b)
    print("%-22s %s" % (label, asc))


show("stored", stored)
show("forward(stored)", forward(stored))
show("backward(stored)", backward(stored))
show("forward sans 20", forward(stored, use_const20=False))
show("backward puis forward", forward(backward(stored)))
