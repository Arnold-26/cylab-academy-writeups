import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p1 = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/220_breadth.v1"
p2 = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/220_breadth.v2"
d1 = open(p1, "rb").read()
d2 = open(p2, "rb").read()
for fo in (0x155ec8, 0x155ef8):
    print(f"0x{fo:x} v1:", d1[fo:fo + 80].split(b"\x00")[0])
    print(f"0x{fo:x} v2:", d2[fo:fo + 80].split(b"\x00")[0])
