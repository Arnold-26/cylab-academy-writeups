#!/bin/bash
P="/mnt/c/Users/arnol/.dsh/attachments/v1/files/43/43be60629ba01766c6880b834d378edabe78a4874cd919efc69631cf32fa932e/torrent.pcap"
cd /tmp || exit 1
timeout 600 tshark -r "$P" -Y "bt-dht" -T fields -e data.data 2>/dev/null > dht.hex
wc -l dht.hex
python3 - <<'PYEOF'
import binascii, re
blob = b""
with open('/tmp/dht.hex') as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                blob += binascii.unhexlify(line)
            except Exception:
                pass
print("taille DHT:", len(blob))
# extraire toutes les chaines lisibles
seen = set()
for m in re.finditer(rb'[ -~]{4,}', blob):
    s = m.group(0)
    if s not in seen:
        seen.add(s)
print("chaines distinctes:", len(seen))
for s in sorted(seen):
    print("  ", s.decode('latin-1')[:100])
PYEOF
