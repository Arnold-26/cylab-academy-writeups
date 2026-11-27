import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/0b369ed5974a5e777ca3bc323bd39d75a6f27762a449d16cd2a0ffc08b2a6aa8/timeline-1-partition4.img.gz"
dest = B / "721_timeline.img.gz"
for attempt in range(6):
    try:
        r = requests.get(u, timeout=120, verify=False, stream=True)
        total = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
                total += len(chunk)
        print("ok", total)
        break
    except Exception as e:
        print("essai", attempt + 1, type(e).__name__)
        time.sleep(4)
if dest.exists():
    print("taille finale:", dest.stat().st_size)
