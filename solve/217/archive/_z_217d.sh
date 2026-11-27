#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 217_homework
echo "--- 4 lignes de A ---"
printf 'AAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAA\n' | timeout 20 ./217_homework 2>&1 | head -20
echo "--- 4 lignes vides ---"
printf '\n\n\n\n' | timeout 20 ./217_homework 2>&1 | head -20
echo "--- 1 ligne ---"
printf '1 2 3\n' | timeout 20 ./217_homework 2>&1 | head -20
