import sys, struct, datetime, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\432_original.jpg"
d = open(p, "rb").read()
# 2023-11-20 20:46:21 UTC (21:46:21 +01:00)
dt = datetime.datetime(2023, 11, 20, 20, 46, 21, tzinfo=datetime.UTC)
epoch = int(dt.timestamp())
print("epoch attendu:", epoch, hex(epoch), "| .420 ms ->", int(dt.timestamp() * 1000))
cands = {
    "u32le": struct.pack("<I", epoch),
    "u32be": struct.pack(">I", epoch),
    "u64le": struct.pack("<Q", epoch),
    "u64be": struct.pack(">Q", epoch),
    "ms u64le": struct.pack("<Q", int(dt.timestamp() * 1000)),
    "ms u64be": struct.pack(">Q", int(dt.timestamp() * 1000)),
}
for name, pat in cands.items():
    idxs = [m.start() for m in re.finditer(re.escape(pat), d)]
    print("%-10s %s -> %d %s" % (name, pat.hex(), len(idxs), idxs[:5]))
# aussi chercher l'offset de la MakerNote
i = d.find(b"Samsung")
print("'Samsung' a:", i)
for m in re.finditer(rb"SEC\x00|SAMSUNG\x00|Samsung", d):
    print("  tag maker:", m.start(), d[m.start():m.start() + 24])
