#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 292_vuln
echo "=== type ==="
file 292_vuln | cut -c1-160
readelf -h 292_vuln | grep -E "Type|Machine"
echo "=== liaisons ==="
ldd 292_vuln 2>&1 | head -5
echo "=== NX / RELRO ==="
python3 - <<'EOF'
from struct import unpack_from
d = open('292_vuln','rb').read()
print("taille:", len(d))
pe = 0
if d[:4] == b'\x7fELF':
    is64 = d[4] == 2
    etype = unpack_from('<H', d, 16)[0]
    print("ELF", "64" if is64 else "32", "type", etype, "(2=EXEC, 3=DYN)")
EOF
echo "=== symboles utiles ==="
nm 292_vuln 2>/dev/null | grep -iE " (system|execve|/bin/sh)$" | head -5
strings -a 292_vuln | grep -c "/bin/sh"
echo "=== gadgets ==="
for g in "pop rdi" "pop rsi" "pop rdx" "syscall" "ret"; do
  printf "%-10s " "$g"
  ROPgadget --binary 292_vuln --only "$g" 2>/dev/null | head -2 | tr '\n' ' ' || echo "(ROPgadget absent)"
  echo
done
