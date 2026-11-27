#!/bin/bash
cd /tmp/office
echo "=== chaines de heap_check ==="
strings -a -t x the_office | grep -E 'Address: %p|Canary: %zu|Heap bottom|Head is not'
echo "=== recherche des xrefs (push <addr>) ==="
for off in $(strings -a -t x the_office | grep -E 'Canary: %zu|Address: %p \(' | awk '{print $1}'); do
  va=$(printf '0x%x' $((0x8048000 + 0x$off)))
  echo "chaine a $va"
  objdump -d -M intel the_office | grep -n "$va" | head -3
done
