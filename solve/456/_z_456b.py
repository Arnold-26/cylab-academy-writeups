import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "/usr/lib/python3/dist-packages")
try:
    from Evtx.Evtx import Evtx
except Exception as e:
    print("err import:", e)
    sys.exit(1)

path = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin/456_Windows_Logs.evtx"
records = []
with Evtx(path) as log:
    for rec in log.records():
        try:
            xml = rec.xml()
        except Exception:
            continue
        records.append(xml)
print("records:", len(records))
# chercher des mots cles
kws = ["academy", "flag", "cmd", "powershell", "shutdown", "schtasks", "Task", "picoCTF"]
hits = 0
for i, xml in enumerate(records):
    low = xml.lower()
    if any(k.lower() in low for k in ("academy", "picoctf", "flag{")):
        print(f"\n--- record {i} ---")
        print(xml[:1200])
        hits += 1
        if hits > 10:
            break
print("hits:", hits)
