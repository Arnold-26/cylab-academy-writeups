#!/bin/bash
B="http://xebec.cylabacademy.net:38430"
echo "=== robots.txt ==="
curl -s -m 20 -i "$B/robots.txt" | head -25
echo
echo "=== index ==="
curl -s -m 20 "$B/" | head -40
