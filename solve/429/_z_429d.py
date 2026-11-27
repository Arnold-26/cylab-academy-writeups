import sys, zipfile, pathlib, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
z = B / "429_WinAntiDbg0x100.zip"
out = B / "win429"
out.mkdir(exist_ok=True)
with zipfile.ZipFile(z) as f:
    for n in f.namelist():
        f.extract(n, out, pwd=b"academy")
    print("fichiers:", f.namelist())
exe = list(out.rglob("*.exe"))
print("exe:", exe)
if exe:
    r = subprocess.run([str(exe[0])], capture_output=True, text=True, timeout=30,
                       input="", cwd=str(exe[0].parent))
    print("=== stdout ===")
    print(r.stdout[:1500])
    print("=== stderr ===")
    print(r.stderr[:500])
    print("code:", r.returncode)
