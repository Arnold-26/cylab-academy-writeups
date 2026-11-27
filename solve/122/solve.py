# 122 - Easy as GDB  (Reverse Engineering, picoCTF 2021)
# Flag: academy{I_5D3_A11DA7_f73c8ead}
# Write-up: ../../../writeups/reverse-engineering/122-easy-as-gdb.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
cy = CyLab(delay=0.4)
cy.login()
for cid in (122, 171):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    desc = ""
    for _ in range(8):
        time.sleep(0.8)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
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
