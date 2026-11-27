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
        if eid != "4688":
            continue
        data = re.findall(r"<Data[^>]*>([^<]*)</Data>", xml)
        # Data[5] = NewProcessName, Data[8] = CommandLine (souvent)
        name = data[5] if len(data) > 5 else ""
        cmd = data[8] if len(data) > 8 else ""
        print(f"\n[{eid}] proc={name!r}")
        print("  data:", [d for d in data if d][:12])
