#!/bin/bash
mkdir -p /tmp/bg2
cd /tmp/bg2
cp ./_z_bg2 . 2>/dev/null
chmod +x _z_bg2
echo "--- files ---"
ls -la /tmp/bg2
echo "--- existing scripts ---"
for f in a b c; do
  echo "=== _z_bg2_$f.sh ==="
  cat ./_z_bg2_$f.sh 2>/dev/null
done
