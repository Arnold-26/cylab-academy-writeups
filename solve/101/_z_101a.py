import sys, json, re, time, subprocess, pathlib, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
BASE = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_wf")
BASE.mkdir(exist_ok=True)
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
cy.req("PUT", "/api/challenges/101/instance/?source=library")
url = None
for _ in range(20):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/101/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
        if urls:
            url = urls[0]
            break
print("101 url:", url)
if url:
    dest = BASE / url.rsplit("/", 1)[-1]
    r = requests.get(url, timeout=120, verify=False)
    dest.write_bytes(r.content)
    print("taille:", dest.stat().st_size)
    # extraire les macros (vbaProject.bin dans le docm = zip)
    import zipfile
    try:
        z = zipfile.ZipFile(dest)
        print("contenu:", z.namelist()[:10])
        for n in z.namelist():
            data = z.read(n)
            m = FLAG.search(data)
            if m:
                print("FLAG dans", n, ":", m.group(0))
            if b"vbaProject" in n.encode() or n.endswith(".bin"):
                txt = data.decode("latin-1", "ignore")
                print(f"--- {n} ---")
                print(txt[:600])
    except Exception as e:
        print("err zip:", e)
