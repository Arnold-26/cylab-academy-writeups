#!/bin/bash
cd /tmp/cylab_re || exit 1
echo "=== refs avec prefixe faux ==="
valgrind --tool=cachegrind --cachegrind-out-file=/dev/null ./149_checkpass 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' 2>&1 | grep 'I   refs' | head -1
echo "=== refs avec academy{ ==="
valgrind --tool=cachegrind --cachegrind-out-file=/dev/null ./149_checkpass 'academy{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}' 2>&1 | grep 'I   refs' | head -1
echo "=== refs avec acadXmy{ ==="
valgrind --tool=cachegrind --cachegrind-out-file=/dev/null ./149_checkpass 'acadXmy{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}' 2>&1 | grep 'I   refs' | head -1
