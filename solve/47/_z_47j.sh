#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== chaines du binaire 47 ==="
strings -n 3 47_investigation-encoded-1-mystery | grep -aE "^[a-z ]{10,}|abcdefghij|flag" | head -10
echo "=== isValid / encode ==="
objdump -d -Mintel 47_investigation-encoded-1-mystery 2>/dev/null | sed -n '/<isValid>:/,/^$/p' | head -25
echo "=== encode ==="
objdump -d -Mintel 47_investigation-encoded-1-mystery 2>/dev/null | sed -n '/<encode>:/,/^$/p' | head -40
