#!/bin/bash
# 57 - B1ll_Gat35  (Reverse Engineering, picoCTF 2019)
# Flag: academy{These are the access codes to the vault: 1063340}
# Write-up: ../../../writeups/reverse-engineering/57-b1ll-gat35.md
# This is the script that produced the flag; historical variants are in archive/.
#
cd /tmp/cylab_eps || exit 1
file 57_win-exec-1.exe | cut -c1-150
echo "=== .NET ? ==="
strings -n 6 57_win-exec-1.exe | grep -aiE "^\.NET|mscoree|System\.|mscorlib|dnlib|Confuser" | head -10
echo "=== chaines interessantes ==="
strings -n 5 57_win-exec-1.exe | grep -aiE "picoCTF|academy|flag|password|correct|wrong|enter|congrat" | head -20
echo "=== taille / sections ==="
python3 - <<'PYEOF'
import struct
p = "/tmp/cylab_eps/57_win-exec-1.exe"
d = open(p,'rb').read()
print("taille:", len(d), "| MZ:", d[:2])
off = struct.unpack('<I', d[0x3c:0x40])[0]
print("PE offset:", hex(off), "| signature:", d[off:off+4])
nsec = struct.unpack('<H', d[off+6:off+8])[0]
print("sections:", nsec)
sh = off + 24 + struct.unpack('<H', d[off+20:off+22])[0]
for i in range(nsec):
    base = sh + i*40
    name = d[base:base+8].rstrip(b'\x00').decode('latin-1')
    vsize = struct.unpack('<I', d[base+8:base+12])[0]
    raw = struct.unpack('<I', d[base+16:base+20])[0]
    rsz = struct.unpack('<I', d[base+20:base+24])[0]
    print("  %-8s vsize=%-8d raw_off=0x%-6x raw_size=%d" % (name, vsize, raw, rsz))
PYEOF
