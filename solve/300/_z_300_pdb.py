import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pdbp = r"./_z_wad300\WinAntiDbg0x300.pdb"
d = open(pdbp, "rb").read()
print("pdb size", len(d))
for pat in (b"academy", b"picoCTF", b"decrypt_flag", b"flag", b"Flag"):
    idx = [m.start() for m in re.finditer(re.escape(pat), d)]
    print(pat, len(idx), idx[:5])

cfg = open(r"./_z_wad300\config.bin", "rb").read()
print("config.bin", len(cfg), cfg.hex())
print(repr(cfg))
