# 131 - Some Assembly Required 2  (Web Exploitation, picoCTF 2021)
# Flag: academy{217f0babdae45710109bb2e6ac1b134a}
# Write-up: ../../../writeups/web-exploitation/131-some-assembly-required-2.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, requests

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

requests.packages.urllib3.disable_warnings()
url = None
for _ in range(15):
    time.sleep(2)
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("desc:", desc[:300].replace("\n", " "))
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
        break
print("131:", url)
if url:
    base = url.rstrip("/")
    r = requests.get(base, timeout=15, verify=False)
    print("page:", re.sub(r"\s+", " ", r.text or "")[:500])
    print("scripts:", re.findall(r'src=["\']([^"\']+)["\']', r.text or "")[:5])
    # recuperer le wasm
    for js in re.findall(r'src=["\']([^"\']+\.js)["\']', r.text or ""):
        rj = requests.get(base + "/" + js.lstrip("/"), timeout=15, verify=False)
        print(f"--- {js} ---")
        print((rj.text or "")[:400])
