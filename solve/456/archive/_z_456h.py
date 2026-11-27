import sys, re, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/tmp/cylab_bin/456_Windows_Logs.evtx"
seen = set()
found = []
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        for name, val in re.findall(r'<Data Name="([^"]+)"[^>]*>([^<]*)</Data>', xml):
            v = (val or "").strip()
            if len(v) < 8 or len(v) > 200:
                continue
            if not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", v):
                continue
            if v in seen:
                continue
            seen.add(v)
            try:
                dec = base64.b64decode(v + "=" * (-len(v) % 4)).decode("ascii")
            except Exception:
                continue
            if not dec.isprintable():
                continue
            found.append((name, v, dec))
for name, v, dec in found:
    print(f"[{name}] {v} -> {dec}")
