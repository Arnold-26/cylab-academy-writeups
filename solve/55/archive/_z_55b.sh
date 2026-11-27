#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== _start -> main ==="
objdump -d -Mintel 55_sice_cream 2>/dev/null | sed -n '/<_start>:/,/^$/p' | grep -E "lea +rdi|call" | head -4
echo "=== chaines ==="
strings -n 5 55_sice_cream | grep -vE "GLIBC|libc|\.so|gmon|stack_chk" | head -25
echo "=== fonctions ==="
objdump -d -Mintel 55_sice_cream 2>/dev/null | grep -E "^0[0-9a-f]+ <" | head -20
