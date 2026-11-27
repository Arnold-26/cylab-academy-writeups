import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"/tmp/cylab_711\encrypt.py")
print(p.read_text(encoding="utf-8", errors="replace"))
