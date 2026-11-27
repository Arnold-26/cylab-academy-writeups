import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "/tmp/cylab_eps/276_keygenme"
d = open(P, "rb").read()
print(d[0x1280:0x1360])
