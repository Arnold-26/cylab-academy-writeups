import sys, re, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
IMG = "/mnt/c/Users/arnol/Downloads/partition4.img"
b64re = re.compile(rb"[A-Za-z0-9+/]{24,}={0,2}")
b32re = re.compile(rb"[A-Z2-7]{24,}={0,6}")
NEEDLES = (b"academy{", b"picoCTF{", b"academy", b"picoCTF")
found = []
seen = set()
CH = 8 * 1024 * 1024
with open(IMG, "rb") as f:
    off = 0
    prev = b""
    while True:
        chunk = f.read(CH)
        if not chunk:
            break
        buf = prev + chunk
        for rx, kind in ((b64re, "b64"), (b32re, "b32")):
            for m in rx.finditer(buf):
                tok = m.group(0)
                if tok in seen or len(tok) > 4000:
                    continue
                seen.add(tok)
                try:
                    if kind == "b64":
                        d = base64.b64decode(tok + b"=" * ((4 - len(tok) % 4) % 4))
                    else:
                        d = base64.b32decode(tok + b"=" * ((8 - len(tok) % 8) % 8))
                except Exception:
                    continue
                for nd in NEEDLES:
                    if nd in d:
                        found.append((off + m.start(), kind, tok[:80], d[:200]))
                        break
        prev = buf[-200:]
        off += len(chunk)
print("candidats:", len(found))
for off, kind, tok, dec in found[:20]:
    print("  %10d %s %r -> %r" % (off, kind, tok[:50], dec[:120]))
