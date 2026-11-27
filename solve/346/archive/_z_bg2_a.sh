#!/bin/bash
B=./_z_bg2
file "$B"
echo "=== checksec-ish ==="
readelf -h "$B" | grep -E 'Type|Entry'
readelf -l "$B" | grep -E 'GNU_STACK|GNU_RELRO'
echo "=== symboles ==="
nm -C "$B" 2>/dev/null | head -40
echo "=== strings utiles ==="
strings -a "$B" | grep -i -E 'move|flag|win|player|L\)|option|command|map|board' | head -20
