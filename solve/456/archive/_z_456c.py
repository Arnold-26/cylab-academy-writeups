import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Evtx.Evtx import Evtx

path = "/tmp/cylab_bin/456_Windows_Logs.evtx"
recs = []
with Evtx(path) as log:
    for rec in log.records():
        try:
            recs.append(rec.xml())
        except Exception:
            pass
print("records:", len(recs))
# extraire EventID + Data
from collections import Counter
ids = Counter()
interesting = []
for xml in recs:
    m = re.search(r"<EventID[^>]*>(\d+)</EventID>", xml)
    eid = m.group(1) if m else "?"
    ids[eid] += 1
    low = xml.lower()
    if any(k in low for k in ("cmd.exe", "powershell", ".exe", "schtasks", "shutdown", "task")):
        interesting.append((eid, xml))
print("top EventIDs:", ids.most_common(15))
print("interessants:", len(interesting))
seen = set()
for eid, xml in interesting[:40]:
    data = re.findall(r"<Data[^>]*>([^<]*)</Data>", xml)
    key = (eid, tuple(data[:4]))
    if key in seen:
        continue
    seen.add(key)
    print(f"\n[{eid}] {data[:8]}")
