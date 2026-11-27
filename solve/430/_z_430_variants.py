data = open("/tmp/winadb/config.bin", "rb").read()
size = int.from_bytes(data[:4], "little")
buf = bytearray(data[4:])
letters = bytes(buf[0:size])
blob = bytes(buf[size + 1:size + 1 + size])


def s8(x):
    x &= 0xFF
    return x - 256 if x > 127 else x


def cmod(a, b):
    r = abs(a) % abs(b)
    return -r if a < 0 else r


def pc(x):
    t = (x & 0x55) + ((x >> 1) & 0x55)
    u = (t & 0x33) + ((t >> 2) & 0x33)
    return (u & 0x0F) + ((u >> 4) & 0x0F)


def apply(s, ch0, mod, reverse=False, sign_pc=1, n=1):
    b = bytearray(s)
    sz = len(b)
    ch = ch0
    idxs = list(range(sz))
    if reverse:
        idxs = idxs[::-1]
    for _ in range(n):
        for j in idxs:
            v = s8(s8(b[j] - ch) + sign_pc * pc(j % 0xFF))
            if mod == "c":
                ch = s8(ch + cmod(v, 26))
            else:
                ch = s8(ch + (v % 26))
            b[j] = ch & 0xFF
    return b


hits = []
for ch0 in (0x61, 0x00, letters[0]):
    for mod in ("c", "p"):
        for rev in (False, True):
            for sg in (1, -1):
                for n in range(1, 4):
                    key = apply(letters, ch0, mod, rev, sg, n)
                    pt = bytes(a ^ b for a, b in zip(blob, key))
                    if b"academy{" in pt or b"picoCTF{" in pt or b"{" in pt:
                        hits.append((ch0, mod, rev, sg, n, pt))
                    # garde aussi les quasi-ASCII
                    if all(32 <= c < 127 for c in pt) and pt[:3] in (b"aca", b"pic"):
                        hits.append(("ASCI", ch0, mod, rev, sg, n, pt))
print("hits:", len(hits))
for h in hits[:10]:
    print(h)
# montrer quelques sorties pour inspection
for ch0 in (0x61, letters[0]):
    for mod in ("c",):
        for rev in (False, True):
            key = apply(letters, ch0, mod, rev, 1, 1)
            print("ch0=%#x mod=%s rev=%s -> %r" % (ch0, mod, rev, bytes(a ^ b for a, b in zip(blob, key))))
