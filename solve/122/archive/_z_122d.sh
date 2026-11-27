#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 122_brute 2>/dev/null | grep -B6 -A4 "0x2037" | head -60
