#!/bin/bash
set -e
B=https://challenge-files.cylabacademy.net/library/61dba8011a3c9577f46bf6cda8bc0de0c5021d574a06f68795aa66e8c15fb6a1/the_office
rm -rf /tmp/office && mkdir -p /tmp/office && cd /tmp/office
curl -sSL -o the_office "$B"
chmod +x the_office
ls -la
file the_office
echo "=== protections ==="
readelf -h the_office | grep -E 'Type|Entry'
readelf -l the_office | grep -E 'GNU_STACK|GNU_RELRO' || true
readelf -d the_office | grep -E 'BIND_NOW|FLAGS' || true
echo "=== strings ==="
strings -a the_office | head -40
