#!/bin/bash
B="http://xebec.cylabacademy.net:43367"
echo "=== POST /auth ==="
curl -s -m 20 -i -c /tmp/jar3.txt -X POST -d "username=test&password=Test123!" "$B/auth" | head -25
echo
echo "=== cookies ==="
cat /tmp/jar3.txt 2>/dev/null | tail -5
echo "=== page apres login ==="
curl -s -m 20 -b /tmp/jar3.txt "$B/" | grep -iE "admin|flag|token|Welcome|jwt" | head -10
