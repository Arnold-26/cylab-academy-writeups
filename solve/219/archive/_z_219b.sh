#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== execution ==="
echo "test" | timeout 10 qemu-riscv64 ./219_riscy 2>&1 | head -5
echo "=== desassemblage ==="
objdump -d -Mintel 219_riscy 2>/dev/null | head -40 || objdump -d 219_riscy 2>/dev/null | head -40
