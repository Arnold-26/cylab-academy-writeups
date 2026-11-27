#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 446_game
echo "=== file ==="
file 446_game | cut -c1-110
echo "=== protections ==="
readelf -h 446_game | grep Type
readelf -s 446_game 2>/dev/null | grep -c stack_chk
echo "=== symboles ==="
nm 446_game 2>/dev/null | grep -E ' T | U ' | head -25
echo "=== strings ==="
strings -n 6 446_game | grep -viE '^(GCC|GLIBC|__|_|\.)' | head -25
