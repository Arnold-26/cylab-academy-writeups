import sys, json, re, requests, pathlib, zipfile
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.7)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
st, b = cy.req("GET", "/api/challenges/528/instance/")
d = json.loads(b)
desc = d.get("description") or ""
print("=== DESC ===")
print(desc[:700])
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    if "challenge-files" in u:
        name = u.rsplit("/", 1)[-1]
        dest = B / f"528_{name}"
        if not (dest.exists() and dest.stat().st_size > 1000):
            r = requests.get(u, timeout=120, verify=False)
            dest.write_bytes(r.content)
        print("fichier:", dest.name, dest.stat().st_size)
        try:
            z = zipfile.ZipFile(dest)
            names = z.namelist()
            print("entrees APK:", len(names))
            for n in names:
                if n.endswith(".dex") or "assets" in n or "res/raw" in n:
                    print("   ", n, z.getinfo(n).file_size)
        except Exception as e:
            print("pas un zip:", type(e).__name__)
