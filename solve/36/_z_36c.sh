#!/bin/bash
cd /tmp/cylab_eps || exit 1
readelf -sW 36_no_auth_mistery 2>/dev/null | grep -iE "secret|indexTable|flag|badChars" | head -10
echo "=== encode / boucle principale ==="
objdump -d -Mintel 36_no_auth_mistery 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '70,140p'
