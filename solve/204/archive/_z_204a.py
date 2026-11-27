import sys, tarfile, pathlib, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
t = tarfile.open(B / "204_notepad.tar")
names = t.getnames()
print("fichiers:", names[:30])
t.extractall(B / "notepad204")
for n in names:
    if n.endswith((".py", ".js", ".php", ".html", ".txt", ".conf", ".yml", ".json")):
        p = B / "notepad204" / n
        if p.is_file() and p.stat().st_size < 20000:
            print(f"\n===== {n} =====")
            print(p.read_text(encoding="utf-8", errors="replace")[:1500])
