#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== 47 output (23 octets) ==="
od -An -tx1 -c 47_investigation-encoded-1-output
echo "=== 36 output (56 octets) ==="
od -An -tx1 -c 36_investigation-encoded-2-output | head -8
echo "=== 47 binary : chaines ==="
strings -n 4 47_investigation-encoded-1-mystery | grep -aiE "flag|png|bmp|jpg|image|open|\.txt" | head -8
echo "=== 47 binary : main ==="
chmod +x 47_investigation-encoded-1-mystery
objdump -d -Mintel 47_investigation-encoded-1-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "add|sub|xor|fputc|fread|fopen|cmp|movzx|shl|shr" | head -25
