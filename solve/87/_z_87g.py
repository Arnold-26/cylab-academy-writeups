import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\87_suspicious.dd.sda1"
with open(p, "rb") as f:
    f.seek(2049 * 1024)
    data = f.read(1024)
buf = data[54:200]
for start in range(52, 60):
    raw = buf[start - 54:]
    n = len(raw) // 2 * 2
    try:
        txt = raw[:n].decode("utf-16le", "replace")
    except Exception:
        continue
    for cand in (txt, txt[::-1]):
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", cand)
        if m:
            print("start=%d -> %r -> FLAG %s" % (start, cand[:80], m.group(0)))
for shift in (0, 1):
    raw = data[55 + shift:]
    raw = raw[:len(raw) // 2 * 2]
    txt = raw.decode("utf-16le", "replace").strip("\x00")
    rev = txt[::-1]
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", rev)
    print("shift=%d rev=%r -> %s" % (shift, rev[:80], m.group(0) if m else None))
