import sys, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
files = {
    "468_token_generator.py": "https://challenge-files.cylabacademy.net/library/db1105bfec855172",
}
# recuperer l'URL exacte depuis la description
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import json, re
cy = CyLab(delay=0.7)
cy.login()
st, b = cy.req("GET", "/api/challenges/468/instance/")
d = json.loads(b)
desc = d.get("description") or ""
print("=== DESC 468 ===")
print(desc[:800])
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    if "challenge-files" in u:
        name = u.rsplit("/", 1)[-1]
        dest = B / f"468_{name}"
        if not (dest.exists() and dest.stat().st_size > 10):
            r = requests.get(u, timeout=30, verify=False)
            dest.write_bytes(r.content)
        print("\n=== %s (%d o) ===" % (name, dest.stat().st_size))
        print(dest.read_text(errors="replace"))
