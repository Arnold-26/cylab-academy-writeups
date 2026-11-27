import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
open(r"./_z_bg2_full.txt", "wb").write(b"l]" + b"w" * 4 + b"d" * 47 + b"w")
print("written", len(open(r"./_z_bg2_full.txt", "rb").read()))
