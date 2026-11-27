#!/bin/bash
B="http://chatelaine.cylabacademy.net:40158"
echo "=== POST /login avec X-Dev-Access ==="
curl -s -m 20 -i -H "X-Dev-Access: yes" -H "Content-Type: application/json" \
  -d '{"email":"ctf-player@cylabacademy.org","password":"x"}' "$B/login" | head -30
echo
echo "=== sans le header (temoin) ==="
curl -s -m 20 -H "Content-Type: application/json" \
  -d '{"email":"ctf-player@cylabacademy.org","password":"x"}' "$B/login" | head -5
