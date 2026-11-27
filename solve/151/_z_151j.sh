#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== ldd ==="
ldd 151_remote 2>&1 | head -12
echo "=== execution ==="
printf 'test\n' | ./151_remote
echo "exit=$?"
echo "=== avec un libcrypto du systeme ==="
ls /usr/lib/x86_64-linux-gnu/libcrypto.so* 2>/dev/null | head -5
