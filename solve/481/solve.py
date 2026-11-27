# 481 - flags are stepic  (Forensics, picoCTF 2025)
# Flag: academy{fl4g_h45_fl4ga947c25f}
# Write-up: ../../../writeups/forensics/481-flags-are-stepic.md
# Script exact utilise pour produire le flag.
#
import sys, json, re, time, requests, pathlib

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

requests.packages.urllib3.disable_warnings()
url = None
for _ in range(20):
    time.sleep(2)
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
            break
print("481:", url)
BASE = pathlib.Path(r"/tmp/cylab_z\481")
BASE.mkdir(parents=True, exist_ok=True)
if url:
    base = url.rstrip("/")
    r = requests.get(base, timeout=15, verify=False)
    imgs = re.findall(r'img:\s*"([^"]+)"', r.text or "")
    print("nb images:", len(imgs))
    S = requests.Session()
    S.headers.update({"User-Agent": "Mozilla/5.0"})
    ok = 0
    for i, rel in enumerate(imgs):
        dest = BASE / rel.replace("flags/", "")
        if dest.exists() and dest.stat().st_size > 0:
            ok += 1
            continue
        try:
            rr = S.get(base + "/" + rel, timeout=20, verify=False)
            if rr.status_code == 200:
                dest.write_bytes(rr.content)
                ok += 1
        except Exception:
            pass
    print("telecharges:", ok)
