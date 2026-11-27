#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 272_vuln
nm 272_vuln 2>/dev/null | grep -E "easy_checker|hard_checker| check$| fun$"
echo "--- desassemblage des adresses ---"
objdump -d -Mintel 272_vuln 2>/dev/null | grep -E "<easy_checker>:|<hard_checker>:" | head -4
echo "--- test local ---"
printf 'AAAAAAAAAAAAAAAAAAAA%%\n-2\n' > /tmp/in272.txt
python3 - <<'EOF'
import subprocess, re
# recuperer les offsets via readelf
out = subprocess.run(["readelf","-sW","272_vuln"], capture_output=True, text=True).stdout
addrs = {}
for line in out.splitlines():
    for nm in ("easy_checker","hard_checker"):
        if nm in line and "FUNC" in line:
            addrs[nm] = int(line.split()[1],16)
print("adresses:", {k: hex(v) for k,v in addrs.items()})
if len(addrs)==2:
    delta = (addrs["easy_checker"] - addrs["hard_checker"])
    print("delta =", delta, "| en int32:", delta - (1<<32) if delta >= (1<<31) else delta)
EOF
