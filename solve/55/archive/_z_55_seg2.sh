#!/bin/bash
grep -n "190fe8" /tmp/libc.asm | head -5
L=$(grep -n "190fe8" /tmp/libc.asm | head -1 | cut -d: -f1)
echo "ligne $L"
sed -n "$((L-45)),$((L+8))p" /tmp/libc.asm
