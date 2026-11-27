#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== gadgets utiles ==="
ROPgadget --binary 214_horse 2>/dev/null | grep -E 'pop rdi ; ret|pop rsi ; ret|pop rdx ; ret|pop rax ; ret|syscall|leave ; ret|pop rsp' | head -20
echo "=== csu ==="
objdump -d -Mintel 214_horse 2>/dev/null | sed -n '/<__libc_csu_init>:/,/^$/p' | head -30
echo "=== sections ==="
readelf -S 214_horse 2>/dev/null | grep -E '\.bss|\.data|\.got'
echo "=== NX ==="
readelf -l 214_horse 2>/dev/null | grep GNU_STACK
