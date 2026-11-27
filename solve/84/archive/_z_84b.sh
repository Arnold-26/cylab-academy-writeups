#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== extraction (dstport, payload) ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "udp && data.data" -T fields -e frame.number -e udp.dstport -e data.data 2>/dev/null > /tmp/84pkts.txt
wc -l /tmp/84pkts.txt
head -12 /tmp/84pkts.txt
python3 - <<'EOF'
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
    rows.append((int(port), db, int(fn)))
print("paquets avec payload:", len(rows))
# 1) ordre des paquets
s1 = b"".join(d for _, d, _ in rows if len(d) == 1)
print("ordre paquets (1 octet):", s1[:120])
# 2) tri par port de destination
one = [(p, d[0]) for p, d, _ in rows if len(d) == 1]
by_port = bytes(c for _, c in sorted(one))
print("tri par port:", by_port[:200])
# 3) tri par port decroissant
by_port_desc = bytes(c for _, c in sorted(one, reverse=True))
print("tri port decroissant:", by_port_desc[:200])
EOF
