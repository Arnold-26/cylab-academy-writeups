#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 172_the_office
file 172_the_office | cut -c1-120
echo "=== symboles ==="
nm 172_the_office 2>/dev/null | grep -E " [Tt] " | head -20
echo "=== chaines ==="
strings -n 6 172_the_office | head -25
echo "=== protections ==="
readelf -lW 172_the_office 2>/dev/null | grep GNU_STACK
readelf -h 172_the_office | grep Type
