#!/bin/bash
cd ./_z_55
echo "=== symboles libc"
readelf -sW libc.so.6 2>/dev/null | grep -E "__malloc_hook|__free_hook|__realloc_hook| main_arena|_IO_2_1_stdout_" | head -10
echo "=== one_gadget dispo ?"
command -v one_gadget || echo ABSENT
echo "=== essai d'execution avec le ld fourni"
cp ../_z_55/sice_cream . 2>/dev/null
printf '4\n' | LD_PRELOAD= ./ld-2.23.so ./sice_cream 2>&1 | head -5
echo "rc=$?"
