#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
for P in "sort=date" "order=date" "sort=amount" "order=amount" "sort=1" "order=1"; do
  printf "=== %s ===\n" "$P"
  curl -s -m 20 -b /tmp/j752.txt -o /tmp/r.txt -w "HTTP %{http_code}\n" "$A/expenses?$P"
  grep -icE "error|traceback|sqlite|syntax" /tmp/r.txt
  grep -oE "<th[^>]*>[^<]*</th>" /tmp/r.txt | head -4
done
echo "=== test quote (erreur ?) ==="
curl -s -m 20 -b /tmp/j752.txt -o /tmp/r2.txt -w "HTTP %{http_code}\n" "$A/expenses?sort='"
grep -icE "error|traceback|sqlite|syntax" /tmp/r2.txt
tail -c 400 /tmp/r2.txt
