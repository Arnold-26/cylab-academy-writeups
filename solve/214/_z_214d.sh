#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== Dockerfile ==="
cat 214_Dockerfile
echo
echo "=== setup debut ==="
objdump -d -Mintel 214_horse 2>/dev/null | sed -n '/<setup>:/,/^$/p' | head -30
echo "=== globaux PAD/HORSE ==="
objdump -d -Mintel 214_horse 2>/dev/null | grep -E '60201|60200' | head -10
echo "=== checksec ==="
readelf -h 214_horse | grep Type
readelf -s 214_horse 2>/dev/null | grep -c stack_chk
