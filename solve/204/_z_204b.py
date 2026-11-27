import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps\notepad204")
print("=== Dockerfile ===")
print((B / "Dockerfile").read_text(encoding="utf-8", errors="replace"))
print("=== static ===")
for p in (B / "static").iterdir():
    print(" ", p.name, p.stat().st_size if p.is_file() else "(dir)")
