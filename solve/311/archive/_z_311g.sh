#!/bin/bash
echo "=== recherche de motifs HTTP / ubuntu / torrent dans le binaire TCP ==="
python3 - <<'PYEOF'
import re
blob = open('/tmp/tcpdata.bin','rb').read()
print("taille:", len(blob))
pats = [b'GET ', b'HTTP/1', b'ubuntu', b'torrent', b'.iso', b'd8:announce', b'4:name', b'BitTorrent', b'\x13BitTorrent']
for p in pats:
    n = blob.count(p)
    print("  %-14r occurrences: %d" % (p, n))
    if n and n < 12:
        for m in re.finditer(re.escape(p), blob):
            s = blob[max(0,m.start()-40):m.start()+120]
            print("      ...", re.sub(rb'[^\x20-\x7e]', b'.', s)[:160])
PYEOF
