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
        if eid not in ("4702", "4699", "106", "140", "200", "201", "129"):
            continue
        data = re.findall(r"<Data[^>]*>([^<]*)</Data>", xml)
        joined = " | ".join(d for d in data if d)
        # afficher seulement si non-Microsoft
        if "Microsoft\\" in joined and "cmd" not in joined.lower() and "powershell" not in joined.lower():
            continue
        print(f"\n[{eid}] {joined[:600]}")
