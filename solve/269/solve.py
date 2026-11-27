# 269 - flag leak  (Binary Exploitation, picoCTF 2022)
# Flag: academy{L34k1ng_Fl4g_0ff_St4ck_9f22d2dd}
# Write-up: ../../../writeups/binary-exploitation/269-flag-leak.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, pathlib, requests

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

requests.packages.urllib3.disable_warnings()
BASE = pathlib.Path(r"/tmp/cylab_bin")
for _ in range(15):
    time.sleep(2)
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("desc:", desc[:400].replace("\n", " "))
        nc = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", desc)
        print("nc:", nc.group(0) if nc else None)
        for u in [x for x in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in x]:
            name = u.rsplit("/", 1)[-1]
            dest = BASE / f"269_{name}"
            if not (dest.exists() and dest.stat().st_size > 0):
                r = requests.get(u, timeout=90, verify=False)
                dest.write_bytes(r.content)
                print("ok:", name, len(r.content))
            else:
                print("deja:", name)
        break
else:
    print("pas demarre")
