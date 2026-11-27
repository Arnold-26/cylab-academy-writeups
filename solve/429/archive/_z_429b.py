import sys, zipfile, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
z = B / "429_WinAntiDbg0x100.zip"
for pw in (b"picoctf", b"infected", b"password", b"malware", None):
    try:
        with zipfile.ZipFile(z) as f:
            names = f.namelist()
            if pw:
                for n in names:
                    f.extract(n, B / "win429", pwd=pw)
            else:
                f.extractall(B / "win429")
        print("OK avec mot de passe:", pw, "| fichiers:", names)
        break
    except Exception as e:
        print("echec", pw, type(e).__name__, str(e)[:60])
p = B / "win429"
if p.exists():
    print([x.name for x in p.rglob("*")])
