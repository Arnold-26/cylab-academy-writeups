#!/bin/bash
P="~/.dsh/attachments/v1/files/43/43be60629ba01766c6880b834d378edabe78a4874cd919efc69631cf32fa932e/torrent.pcap"
cd /tmp || exit 1
timeout 600 tshark -r "$P" -Y "tcp.len>0" -T fields -e data.data 2>/dev/null > tcpdata.hex
wc -l tcpdata.hex
python3 - <<'PYEOF'
import binascii, re
blob = b""
with open('/tmp/tcpdata.hex') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            blob += binascii.unhexlify(line)
        except Exception:
            pass
print("taille des donnees TCP:", len(blob))
open('/tmp/tcpdata.bin','wb').write(blob)
# recherche de chaines
for m in re.finditer(rb'[ -~]{5,}', blob):
    s = m.group(0)
    if b'.iso' in s or b'torrent protocol' in s or b'ut_metadata' in s or b'name' in s.lower()[:20]:
        print("  ", s[:120])
PYEOF
