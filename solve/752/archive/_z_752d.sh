#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
echo "=== /expenses ==="
curl -s -m 20 -b /tmp/j752.txt "$A/expenses" | grep -iE "<form|input|select|sort|order|option|table" | head -20
echo
echo "=== /dashboard ==="
curl -s -m 20 -b /tmp/j752.txt "$A/dashboard" | grep -iE "<form|input|sort|flag|table|th>" | head -15
