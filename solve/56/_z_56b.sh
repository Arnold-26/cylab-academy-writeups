#!/bin/bash
cd /tmp/cylab_eps || exit 1
mkdir -p b1g && cd b1g || exit 1
unzip -o -q ../56_b1g_mac.zip 2>/dev/null
ls -la | head -10
echo "=== file ==="
file main.exe | cut -c1-120
echo "=== strings ==="
strings -n 5 main.exe 2>/dev/null | grep -viE '^(GCC|GLIBC|__|_|\.)' | head -25
echo "=== .NET ? ==="
strings -n 4 main.exe | grep -iE 'mscoree|BSJB|\.NET' | head -5
