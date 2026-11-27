#!/bin/bash
cd /tmp/office
echo "=== offsets des chaines cles ==="
strings -a -t x the_office | grep -E 'admin|Not admin|flag.txt|Unable to open|Get access token|Employee #'
echo "=== recherche des VAs dans le code ==="
for s in admin 'Not admin' 'flag.txt' 'Unable to open' 'Employee #?'; do
  off=$(strings -a -t x the_office | grep -F "$s" | head -1 | awk '{print $1}')
  [ -z "$off" ] && continue
  va=$(printf '0x%x' $((0x8048000 + 0x$off)))
  echo "--- '$s' @ $va ---"
  grep -n "$va" asm.txt | head -4
done
