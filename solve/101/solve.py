# 101 - Weird File  (Forensics, picoCTF 2021)
# Flag: academy{m4cr0s_r_d4ng3r0us}
# Write-up: ../../../writeups/forensics/101-weird-file.md
# Script exact utilise pour produire le flag.
#
import sys, json, re, time, subprocess, pathlib, requests

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

requests.packages.urllib3.disable_warnings()
BASE = pathlib.Path(r"/tmp/cylab_wf")
BASE.mkdir(exist_ok=True)
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
url = None
for _ in range(20):
    time.sleep(2)
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
