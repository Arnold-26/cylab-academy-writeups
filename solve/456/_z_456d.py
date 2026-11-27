import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin/456_Windows_Logs.evtx"
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        m = re.search(r"<EventID[^>]*>(\d+)</EventID>", xml)
        eid = m.group(1) if m else "?"
        if eid in ("4688", "1102", "104", "6", "200", "106", "4702"):
            data = re.findall(r"<Data[^>]*>([^<]*)</Data>", xml)
            print(f"\n[{eid}] {data[:10]}")
