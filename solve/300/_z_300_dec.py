import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

cfg = open(r"./_z_wad300\config.bin", "rb").read()
L = int.from_bytes(cfg[:4], "little")
first = cfg[4:4 + L]
second = cfg[4 + L + 1:4 + L + 1 + L + 1]
print("L", L)
print("first ", first)
print("second", second.hex(), len(second))


def cdiv_rem(a, b):
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return a - q * b


def dec1(buf, rounds):
    b = bytearray(buf)
    n = len(b)
    for _ in range(rounds):
        for j in range(n):
            t = ((j % 255) & 0x55) + (((j % 255) >> 1) & 0x55)
            u = (0x33 & t) + ((t >> 2) & 0x33)
            a = 0x61
            c = b[j] - a
            c += (0x0f & u)
            c += ((u >> 4) & 0x0f)
            rem = cdiv_rem(c, 0x1a)
            b[j] = (a + rem) & 0xff
    return bytes(b)


for rounds in range(1, 9):
    key = dec1(first, rounds)
    flag = bytes(x ^ y for x, y in zip(second, key))
    print(rounds, key, "|", flag)
