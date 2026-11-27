import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/tmp/cylab_bin/456_Windows_Logs.evtx"
shown = 0
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        m = re.search(r"<EventID[^>]*>(\d+)</EventID>", xml)
        eid = m.group(1) if m else "?"
        if eid in ("1033", "1040", "1042"):
            print(f"\n===== EventID {eid} =====")
            print(xml[:2500])
            shown += 1
            if shown >= 2:
                break
