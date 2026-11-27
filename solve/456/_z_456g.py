import sys, re, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/tmp/cylab_bin/456_Windows_Logs.evtx"
parts = []
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        m = re.search(r"<EventID[^>]*>(\d+)</EventID>", xml)
        eid = m.group(1) if m else "?"
        if eid not in ("1033", "4657", "1074"):
            continue
        data = re.findall(r'<Data Name="([^"]+)"[^>]*>([^<]*)</Data>', xml)
        print(f"\n=== EventID {eid} ===")
        for name, val in data:
            if len(val) > 8 and re.fullmatch(r"[A-Za-z0-9+/=]{8,}", val or ""):
                print(f"  [{name}] base64: {val[:120]}")
                try:
                    dec = base64.b64decode(val + "=" * (-len(val) % 4)).decode("utf-8", "replace")
                    print(f"     -> {dec}")
                    parts.append(dec)
                except Exception:
                    pass
            elif name in ("Manufacturer", "NewValue", "Comment", "Data"):
                print(f"  [{name}] {val[:150]}")
print("\nparts:", parts)
