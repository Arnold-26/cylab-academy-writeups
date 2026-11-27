import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps" + "\\"
for f in ("27_investigative-reversing-1-mystery.png",
          "27_investigative-reversing-1-mystery2.png",
          "27_investigative-reversing-1-mystery3.png",
          "70_investigative-reversing-0-mystery.png"):
    d = open(base + f, "rb").read()
    i = d.rfind(b"IEND")
    tail = d[i + 8:] if i >= 0 else b""
    print("%-42s taille=%-8d tail=%d %r" % (f, len(d), len(tail), tail))
