# 122 - Easy as GDB  (Reverse Engineering, picoCTF 2021)
# Flag: academy{I_5D3_A11DA7_f73c8ead}
# Write-up: ../../../writeups/reverse-engineering/122-easy-as-gdb.md
# Script exact utilise pour produire le flag.
#
import sys, re, json, time, requests, urllib3, pathlib

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
for cid in (122, 171):
    desc = ""
    for _ in range(8):
        time.sleep(0.8)
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        if "challenge-files" in desc or "nc " in desc:
            break
    print("=== %d ===" % cid)
    print(desc[:350].replace("\n", " "))
    for u in re.findall(r"https?://[^\s'\"<>]+", desc):
        name = u.rsplit("/", 1)[-1]
        dest = B / f"{cid}_{name}"
        try:
            r = requests.get(u, timeout=90, verify=False)
            dest.write_bytes(r.content)
            print("   ok", dest.name, len(r.content))
        except Exception as e:
            print("   err", name, type(e).__name__)
    print()
