#!/bin/bash
cd /tmp/office
echo "=== strings (apres le menu) ==="
strings -a the_office | sed -n '35,90p'
echo "=== execution locale (menu) ==="
printf '0\n' | timeout 5 ./the_office 2>&1 | head -40
echo "=== code de sortie: $? ==="
