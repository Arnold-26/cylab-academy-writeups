#!/bin/bash
B="http://xebec.cylabacademy.net:43367"
echo "=== page ==="
curl -s -m 20 "$B/" | grep -iE "<form|input|button|script|fetch|action" | head -15
echo
echo "=== login test/Test123! ==="
curl -s -m 20 -i -c /tmp/jar.txt -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!"}' "$B/api/login" 2>/dev/null | head -20
echo "--- variante /login ---"
curl -s -m 20 -i -c /tmp/jar2.txt -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!"}' "$B/login" 2>/dev/null | head -20
