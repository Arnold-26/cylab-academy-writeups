import sys, re, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
IMG = "/mnt/c/Users/arnol/Downloads/partition4.img"
rx = re.compile(rb"[A-Za-z0-9+/]{16,120}={0,2}")
seen = set()
out = []
CH = 8 * 1024 * 1024
prev = b""
off = 0
with open(IMG, "rb") as f:
    while True:
        chunk = f.read(CH)
        if not chunk:
            break
        buf = prev + chunk
        for m in rx.finditer(buf):
            tok = m.group(0)
            if tok in seen:
                continue
            seen.add(tok)
            try:
                dec = base64.b64decode(tok + b"=" * ((4 - len(tok) % 4) % 4))
            except Exception:
                continue
            if len(dec) < 8:
                continue
            printable = sum(1 for c in dec if 32 <= c < 127)
            if printable / len(dec) > 0.95:
                s = dec.decode("latin-1")
                if any(ch.isalpha() for ch in s) and (s.isprintable()):
                    out.append(s)
        prev = buf[-200:]
        off += len(chunk)
print("candidats imprimables:", len(out))
for s in out[:60]:
    print("  ", s[:110])
