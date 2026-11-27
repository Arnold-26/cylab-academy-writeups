#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== _start pour trouver main ==="
objdump -d -Mintel --start-address=0x8049000 --stop-address=0x8049090 181_vuln 2>/dev/null | grep -E "mov +edi|call" | head -6
echo "=== zone 0x80491f0 - 0x80492d0 ==="
objdump -d -Mintel --start-address=0x80491f0 --stop-address=0x80492d0 181_vuln 2>/dev/null | grep -vE "^$" | head -40
echo "=== reference a flag.txt ==="
objdump -d -Mintel 181_vuln 2>/dev/null | grep -B4 "fopen@plt" | head -20
