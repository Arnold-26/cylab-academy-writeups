#!/bin/bash
cd /tmp/winadb
objdump -d -M intel u300.exe > /tmp/u300.asm 2>/dev/null
echo "=== appels a DecryptFlag (0x402cb0)"
grep -n "call.*402cb0" /tmp/u300.asm
L=$(grep -n "call.*402cb0" /tmp/u300.asm | head -1 | cut -d: -f1)
echo "=== contexte avant l'appel (ligne $L)"
sed -n "$((L-45)),$((L+12))p" /tmp/u300.asm
