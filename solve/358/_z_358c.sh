#!/bin/bash
cd /mnt/d/ctf-index || exit 1
python3 _z_358b.py 2>&1 | tail -5
read H P < _z_358url.txt
echo "host=$H port=$P"
echo "=== homepage ==="
curl -s -m 20 "http://${H}:${P}/" | head -40
