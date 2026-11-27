import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sstv
print("dir:", [x for x in dir(sstv) if not x.startswith("_")])
print("version:", getattr(sstv, "__version__", "?"))
