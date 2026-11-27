#!/bin/bash
cd /tmp/cylab_eps || exit 1
cp ./_z_hook.c hook.c
sed -i '1i #include <dlfcn.h>' hook.c
gcc -shared -fPIC -o hook.so hook.c -ldl 2>&1 | head -5
echo "=== run avec hook ==="
echo "test123" | LD_PRELOAD=./hook.so ./276_keygenme 2>&1 | head -20
