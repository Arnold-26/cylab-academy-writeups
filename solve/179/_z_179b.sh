#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin || exit 1
echo "=== gadgets ==="
ROPgadget --binary 179_vuln --only "pop|ret" 2>/dev/null | grep -E "pop rdi ; ret" | head -3
echo "=== ret ==="
ROPgadget --binary 179_vuln --only "ret" 2>/dev/null | head -3
echo "=== GOT puts ==="
objdump -R 179_vuln 2>/dev/null | grep -E "puts|read"
echo "=== plt ==="
objdump -d -Mintel 179_vuln | grep -E "<puts@plt>|<read@plt>|<do_stuff>|<main>" | head -8
