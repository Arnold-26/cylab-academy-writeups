#!/bin/bash
B="http://chatelaine.cylabacademy.net:40158"
echo "=== scripts / fetch ==="
curl -s -m 20 "$B/" | grep -nE "fetch|axios|XMLHttpRequest|action|/login|/api|script" | head -20
echo
echo "=== essais d'endpoints ==="
for E in /login /api/login /auth /api/auth; do
  printf "%s -> " "$E"
  curl -s -m 15 -o /dev/null -w "%{http_code}\n" -H "X-Dev-Access: yes" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"ctf-player@cylabacademy.org\",\"password\":\"x\"}" "$B$E"
done
