import sys, re, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = []
for line in open("/tmp/84pkts.txt"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 3:
        continue
    fn, port, data = parts[0], parts[1], parts[2]
    if not port or not data:
        continue
    try:
        db = bytes.fromhex(data)
    except Exception:
        continue
    rows.append((int(fn), int(port), db))
print("ports:", collections.Counter(p for _, p, _ in rows))
for port in sorted(set(p for _, p, _ in rows)):
    seq = b"".join(d for _, p, d in rows if p == port and len(d) == 1)
    if seq:
        print("\n--- port %d (%d octets) ---" % (port, len(seq)))
        print(seq[:300])
