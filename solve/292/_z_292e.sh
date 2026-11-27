#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
for A in 0x80498ca 0x8049a96 0x8049ad1 0x8049cd3; do
  echo "=== gadget autour de $A ==="
  objdump -d -Mintel --start-address=$((A)) --stop-address=$((A+16)) 292_vuln 2>/dev/null | tail -8
done
echo "=== recherche 'mov edx, imm32' (BA + 4 octets + C3) ==="
python3 - <<'EOF'
d = open('292_vuln','rb').read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF+SZ]
out = []
for i in range(len(t)-6):
    if t[i] == 0xBA and t[i+5] == 0xC3:
        out.append((VA+i, int.from_bytes(t[i+1:i+5], 'little')))
    if len(out) >= 8:
        break
print([(hex(a), v) for a, v in out])
EOF
