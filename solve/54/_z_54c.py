import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\t54"
import os
B = os.path.join(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps", "t54") if os.path.isdir(os.path.join(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps", "t54")) else "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t54"
for i in range(1, 6):
    pa = os.path.join(B, "encA0%d.bmp" % i)
    pb = os.path.join(B, "encB0%d.bmp" % i)
    a = open(pa, "rb").read()
    b = open(pb, "rb").read()
    diffs = [x for x in range(min(len(a), len(b))) if a[x] != b[x]]
    print("image %d: %d octets differents" % (i, len(diffs)))
    print("   premiers:", diffs[:12], "| dernier:", diffs[-1] if diffs else None)
    if diffs:
        st = set(diffs[x + 1] - diffs[x] for x in range(len(diffs) - 1))
        print("   strides:", sorted(st)[:8])
