import sys, json, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.7)
cy.login()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
st, b = cy.req("GET", "/api/challenges/529/instance/")
d = json.loads(b)
desc = d.get("description") or ""
print("=== DESC 529 (complet) ===")
print(desc)
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    print("URL:", u)
    if "challenge-files" in u:
        name = u.rsplit("/", 1)[-1]
        dest = B / f"529_{name}"
        if not (dest.exists() and dest.stat().st_size > 1000):
            try:
                r = requests.get(u, timeout=120, verify=False)
                dest.write_bytes(r.content)
            except Exception as e:
                print("  err", type(e).__name__)
        if dest.exists():
            print("  fichier:", dest.name, dest.stat().st_size)
