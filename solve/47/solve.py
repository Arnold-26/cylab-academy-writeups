# 47 - investigation_encoded_1  (Forensics, picoCTF 2019)
# Flag: academy{...}
# Write-up: ../../../writeups/forensics/47-investigation-encoded-1.md
# Script exact utilise pour produire le flag.
#
import sys, struct, json

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"/tmp/cylab_eps\47_investigation-encoded-1-mystery"
OUT = r"/tmp/cylab_eps\47_investigation-encoded-1-output"
d = open(BIN, "rb").read()
secret = d[0x2020:0x2020 + 37]
matrix = struct.unpack("<54i", d[0x2060:0x2060 + 216])
codes = {}
for k in range(27):
    ln, off = matrix[2 * k], matrix[2 * k + 1]
    if 0 < ln < 24 and 0 <= off < 296:
        b = "".join(str((secret[(off + j) // 8] >> (7 - (off + j) % 8)) & 1) for j in range(ln))
        codes.setdefault(b, k)
enc = open(OUT, "rb").read()


def decode(bitstr):
    out = []
    i = 0
    while i < len(bitstr):
        hit = None
        for L in range(1, 25):
            if i + L > len(bitstr):
                break
            if bitstr[i:i + L] in codes:
                hit = (L, codes[bitstr[i:i + L]])
                break
        if hit is None:
            break
        L, k = hit
        out.append(chr(ord("a") + k) if k < 26 else " ")
        i += L
    return "".join(out), len(bitstr) - i


variants = {}
variants["normal"] = "".join(format(x, "08b") for x in enc)
variants["bytes_rev"] = "".join(format(x, "08b") for x in enc[::-1])
variants["bits_rev"] = "".join(format(x, "08b") for x in enc)[::-1]
for name, bs in variants.items():
    s, left = decode(bs)
    print("%-10s -> %r (reste %d)" % (name, s, left))
    variants[name + "_str"] = s

seen = set()
for name, s in variants.items():
    if not isinstance(s, str):
        continue
    body = s.strip().replace(" ", "")
    for cand in (body, body[::-1]):
        if not cand or cand in seen:
            continue
        seen.add(cand)
        f = "academy{%s}" % cand
        try:
            ok = json.loads(b).get("correct")
        except Exception:
            ok = None
        print("  %-36s -> %s" % (f, ok))
        if ok:
            print("FLAG:", f)
            sys.exit(0)
