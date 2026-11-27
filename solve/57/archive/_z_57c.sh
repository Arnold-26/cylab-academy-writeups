#!/bin/bash
cd /tmp/cylab_eps || exit 1
export WINEDEBUG=-all
echo "=== execution avec 'test' ==="
printf 'test\n' | timeout 60 wine 57_win-exec-1.exe 2>/dev/null | head -20
echo "=== avec un nombre ==="
printf '5\n' | timeout 60 wine 57_win-exec-1.exe 2>/dev/null | head -20
