#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== symboles de donnees ==="
nm 47_investigation-encoded-1-mystery 2>/dev/null | grep -iE "secret|matrix|flag_|buff" | head -10
readelf -sW 47_investigation-encoded-1-mystery 2>/dev/null | grep -iE "secret|matrix" | head -10
echo "=== sections ==="
readelf -SW 47_investigation-encoded-1-mystery 2>/dev/null | grep -E "\.data|\.bss|\.rodata" | head -5
