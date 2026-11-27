import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\383_disk.img"
OFF = 731136 * 512
BLK = 56274
with open(p, "rb") as f:
    f.seek(OFF + BLK * 4096)
    data = f.read(4096)
print("lu:", len(data))
print("debut:", data[:20])
slack = data[12:]
nz = slack.rstrip(b"\x00")
print("slack non nul:", len(nz))
print("repr:", nz[:600])
print("hex:", nz[:200].hex())
