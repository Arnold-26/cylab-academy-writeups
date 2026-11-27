#!/bin/bash
echo "=== err4.txt ==="
cat /tmp/err4.txt 2>/dev/null
echo "=== verified4 head ==="
head -c 100 /mnt/d/ctf-index/_z_496_emls/verified4.eml
echo
echo "=== rerun ==="
cd /tmp || exit 1
node /mnt/d/ctf-index/_z_496_osverify.js /mnt/d/ctf-index/_z_496_emls/real_reply4.eml /mnt/d/ctf-index/_z_496_emls/ca.crt > /tmp/o.txt 2> /tmp/e.txt
echo "STDOUT(first 80):"
head -c 80 /tmp/o.txt
echo
echo "STDERR:"
cat /tmp/e.txt
echo "STDOUT bytes: $(wc -c < /tmp/o.txt)"
