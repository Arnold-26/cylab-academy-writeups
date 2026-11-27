#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 - <<'EOF'
import subprocess
out = subprocess.run(["tshark", "-r", "84_shark-on-wire-2-capture.pcap",
                      "-Y", "data.len==1", "-T", "fields",
                      "-e", "frame.number", "-e", "ip.src", "-e", "ip.dst",
                      "-e", "udp.dstport", "-e", "data.data"],
                     capture_output=True, text=True).stdout
rows = [l.split("\t") for l in out.strip().split("\n") if l.strip()]
rows = [r for r in rows if len(r) >= 5 and r[4]]
# exclure les ports 8990 (bruit zzz/fff) et garder 8888
keep = [r for r in rows if r[3] == "8888"]
print("paquets 8888:", len(keep))
# trier par destination puis frame
keep.sort(key=lambda r: (r[2], int(r[0])))
s = "".join(bytes.fromhex(r[4]).decode("latin1") for r in keep)
print("par dest puis trame:", s)
# affichage detaille
cur = None
buf = ""
for r in keep:
    if r[2] != cur:
        if cur:
            print(f"  {cur}: {buf}")
        cur = r[2]
        buf = ""
    buf += bytes.fromhex(r[4]).decode("latin1")
if cur:
    print(f"  {cur}: {buf}")
EOF
