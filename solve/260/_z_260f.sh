#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== prologue de vuln ==="
objdump -d -Mintel 260_vuln 2>/dev/null | sed -n '/<vuln>:/,+8p'
echo "=== epilogue (fin de vuln) ==="
objdump -d -Mintel 260_vuln 2>/dev/null | sed -n '/<vuln>:/,/^$/p' | tail -25
