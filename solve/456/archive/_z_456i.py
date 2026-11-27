import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/tmp/cylab_bin/456_Windows_Logs.evtx"
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        if "Manufacturer" in xml or "Comment" in xml or "param6" in xml:
            m = re.search(r"<EventID[^>]*>(\d+)</EventID>", xml)
            eid = m.group(1) if m else "?"
            print(f"\n=== EventID {eid} ===")
            for name, val in re.findall(r'<Data Name="([^"]+)"[^>]*>([^<]*)</Data>', xml):
                print(f"  [{name}] {val[:200]}")
