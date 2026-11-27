import sys, re, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/tmp/cylab_bin/456_Windows_Logs.evtx"
seen = set()
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        for name, val in re.findall(r'<Data Name="([^"]+)"[^>]*>([^<]*)</Data>', xml):
            v = (val or "").strip()
            if len(v) < 6 or v in seen:
                continue
            if "_" in v or "{" in v or "}" in v or "pico" in v.lower() or "academy" in v.lower():
                seen.add(v)
                print(f"[{name}] {v[:200]}")
