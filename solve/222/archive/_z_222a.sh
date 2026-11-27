#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== mitations ==="
readelf -l 222_not-crypto 2>/dev/null | grep -E 'GNU_RELRO|GNU_STACK'
readelf -d 222_not-crypto 2>/dev/null | grep -E 'BIND_NOW'
echo "=== symbols ==="
nm 222_not-crypto 2>/dev/null | head -20
echo "=== strings utiles ==="
strings -n 5 222_not-crypto | grep -vE '^(GCC|GLIBC|__|\.|[A-Za-z_]+@@)' | head -25
echo "=== main ==="
objdump -d -Mintel 222_not-crypto 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -60
