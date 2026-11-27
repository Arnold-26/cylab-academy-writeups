import sys, re, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path


def parse_der_int(b, i):
    assert b[i] == 0x02, "attendu INTEGER, vu %02x a %d" % (b[i], i)
    ln = b[i + 1]
    i += 2
    if ln & 0x80:
        nb = ln & 0x7F
        ln = int.from_bytes(b[i:i + nb], "big")
        i += nb
    val = int.from_bytes(b[i:i + ln], "big")
    return val, i + ln


def parse_key(path):
    txt = Path(path).read_text()
    b64 = "".join(l for l in txt.splitlines() if l and not l.startswith("-----"))
    der = base64.b64decode(b64)
    # SEQUENCE
    i = 0
    assert der[0] == 0x30
    ln = der[1]
    i = 2
    if ln & 0x80:
        nb = ln & 0x7F
        i = 2 + nb
    ver, i = parse_der_int(der, i)
    vals = []
    for _ in range(8):
        v, i = parse_der_int(der, i)
        vals.append(v)
    n, e, d, p, q, dp, dq, qinv = vals
    return dict(ver=ver, n=n, e=e, d=d, p=p, q=q, dp=dp, dq=dq, qinv=qinv)


for cid in (207, 211):
    k = parse_key(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\pm_%d\private.key" % cid)
    print("=== %d ===" % cid)
    print("  n bits:", k["n"].bit_length(), "| e:", k["e"])
    print("  p*q == n ?", k["p"] * k["q"] == k["n"])
    print("  p bits/pairs:", k["p"].bit_length(), k["q"].bit_length())
    print("  dp ok ?", k["dp"] == k["d"] % (k["p"] - 1) if k["p"] else None)
    print("  dq ok ?", k["dq"] == k["d"] % (k["q"] - 1) if k["q"] else None)
    print("  qinv*p % q == 1 ?", (k["qinv"] * k["p"]) % k["q"] == 1 if k["q"] else None)
    print("  ver:", k["ver"])
