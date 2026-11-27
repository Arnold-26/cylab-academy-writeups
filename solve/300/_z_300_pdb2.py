import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d = open(r"D:\ctf-index\_z_wad300\WinAntiDbg0x300.pdb", "rb").read()
for off in (54052, 55010, 645210, 651943, 661963):
    print("=" * 20, off)
    print(repr(d[max(0, off - 200):off + 260]))
