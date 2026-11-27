import sys, json, re, time, subprocess, pathlib, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
BASE = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_iw")
BASE.mkdir(exist_ok=True)
cy.req("PUT", "/api/challenges/354/instance/?source=library")
url = None
for _ in range(20):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/354/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
        print("desc:", desc[:300].replace("\n", " "))
        if urls:
            url = urls[0]
            break
print("354 url:", url)
if url:
    dest = BASE / url.rsplit("/", 1)[-1]
    r = requests.get(url, timeout=180, verify=False)
    dest.write_bytes(r.content)
    print("taille:", dest.stat().st_size)
