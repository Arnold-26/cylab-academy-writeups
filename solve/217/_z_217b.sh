#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== main ==="
objdump -d -Mintel 217_homework 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -80
