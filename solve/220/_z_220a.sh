#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== file ==="
file 220_breadth.v1 220_breadth.v2 2>/dev/null | cut -c1-110
echo "=== taille/hash ==="
md5sum 220_breadth.v1 220_breadth.v2 2>/dev/null
ls -la 220_breadth.v1 220_breadth.v2
echo "=== strings v1 (filtre) ==="
strings -n 6 220_breadth.v1 2>/dev/null | grep -viE '^(GCC|GLIBC|__|_|\.)' | head -15
echo "=== strings v2 (filtre) ==="
strings -n 6 220_breadth.v2 2>/dev/null | grep -viE '^(GCC|GLIBC|__|_|\.)' | head -15
