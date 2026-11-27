#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 - <<'EOF'
import subprocess
out = subprocess.run(["tshark", "-r", "84_shark-on-wire-2-capture.pcap",
                      "-Y", "data.len==1", "-T", "fields",
                      "-e", "frame.number", "-e", "ip.src", "-e", "ip.dst",
                      "-e", "udp.srcport", "-e", "udp.dstport", "-e", "data.data"],
                     capture_output=True, text=True).stdout
rows = [l.split("\t") for l in out.strip().split("\n") if l.strip()]
print("total:", len(rows))
from collections import Counter
combos = Counter((r[1], r[2], r[3], r[4]) for r in rows if len(r) >= 6)
for c, n in combos.most_common(10):
    print(c, n)
# toutes les chaines par (src,dst,ports)
for combo in combos:
    s = "".join(bytes.fromhex(r[5]).decode("latin1") for r in rows
                if len(r) >= 6 and (r[1], r[2], r[3], r[4]) == combo and r[5])
    print(f"\n{combo} ({len(s)}):")
    print(s[:200])
EOF
