#!/bin/bash
cd /tmp/cylab_eps || exit 1
tshark -r 84_shark-on-wire-2-capture.pcap -Y "udp.dstport==8888 && data.data && frame.len < 100" \
  -T fields -e frame.number -e ip.id -e ip.ttl -e udp.length -e ip.len -e data.data 2>/dev/null > /tmp/84p8888.txt
wc -l /tmp/84p8888.txt
head -10 /tmp/84p8888.txt
python3 - <<'EOF'
rows = []
for line in open("/tmp/84p8888.txt"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 6:
        continue
    fn, ipid, ttl, ulen, iplen, data = p[:6]
    try:
        db = bytes.fromhex(data)
    except Exception:
        continue
    rows.append({"fn": int(fn), "ipid": int(ipid, 16) if ipid else 0,
                 "ttl": int(ttl) if ttl else 0, "ulen": int(ulen) if ulen else 0,
                 "iplen": int(iplen) if iplen else 0, "d": db})
print("lignes:", len(rows))
for key in ("fn", "ipid", "ttl", "ulen", "iplen"):
    seq = b"".join(r["d"] for r in sorted(rows, key=lambda r: r[key]))
    print("%-6s -> %s" % (key, seq.decode("latin-1", "replace")))
EOF
