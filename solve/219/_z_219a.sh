#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== file ==="
file 219_riscy | cut -c1-130
echo "=== outils riscv ==="
which qemu-riscv64 qemu-riscv64-static riscv64-linux-gnu-objdump 2>/dev/null
echo "=== strings ==="
strings -n 4 219_riscy | head -20
echo "=== entete ==="
readelf -h 219_riscy 2>/dev/null | head -20
