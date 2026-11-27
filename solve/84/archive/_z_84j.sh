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
rows = [r for r in rows if len(r) >= 6 and r[5]]
print("total 1 octet:", len(rows))
# ordre de trame
s = "".join(bytes.fromhex(r[5]).decode("latin1") for r in rows)
print("\nordre trame:", s)
# detail par trame pour les 8888
print("\n=== paquets 8888 ===")
for r in rows:
    if r[4] == "8888":
        print(r[0], r[1], "->", r[2], repr(bytes.fromhex(r[5]).decode("latin1")))
EOF
