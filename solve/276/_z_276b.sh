#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== toutes les chaines imprimables de .rodata ==="
objdump -s -j .rodata 276_keygenme 2>/dev/null | head -30
echo "=== chaines courtes ==="
strings -n 3 276_keygenme | grep -viE '^(GCC|GLIBC|__|_|\.|OPENSSL)' | head -40
