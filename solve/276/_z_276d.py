import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "/tmp/cylab_eps/276_keygenme"
d = open(P, "rb").read()
# trouver les adresses des morceaux
for s in (b"academy{H", b"br1ng_y0H", b"g_y0ur_0H", b"wn_k3y_", b"dH"):
    i = d.find(s)
    print(s, "offset", hex(i) if i >= 0 else None)
# section .data
r = subprocess.run(["readelf", "-S", P], capture_output=True, text=True).stdout
for line in r.split("\n"):
    if ".data" in line or ".bss" in line or ".text" in line:
        print(line.strip())
