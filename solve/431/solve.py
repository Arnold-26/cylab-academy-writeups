# 431 - WinAntiDbg0x300  (Reverse Engineering, picoCTF 2024)
# Flag: academy{Wind0ws_antid3bg_0x300_f57a6e29}
# Write-up: ../../../writeups/reverse-engineering/431-winantidbg0x300.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, requests, pathlib, zipfile

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
desc = ""
for _ in range(10):
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    if "challenge-files" in desc:
        break
    time.sleep(0.4)
print(desc[:800])
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    name = u.rsplit("/", 1)[-1]
    dest = B / f"431_{name}"
    if dest.exists() and dest.stat().st_size > 100:
        print("deja", dest.name, dest.stat().st_size)
        continue
    try:
        r = requests.get(u, timeout=90, verify=False)
        dest.write_bytes(r.content)
        print("ok", dest.name, len(r.content))
        if name.endswith(".zip"):
            out = B / "win431"
            out.mkdir(exist_ok=True)
            mwp = re.search(r"password `([^`]+)`", desc)
            pwd = mwp.group(1) if mwp else "academy"
            with zipfile.ZipFile(dest) as f:
                for n in f.namelist():
                    f.extract(n, out, pwd=pwd.encode())
            print("  extrait:", [p.name for p in out.rglob("*")])
    except Exception as e:
        print("err", name, type(e).__name__, str(e)[:60])
