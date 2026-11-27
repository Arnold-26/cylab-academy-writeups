#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
echo "=== inscription ==="
curl -s -m 20 -i -c /tmp/j752.txt -d "username=hacker1&email=h1@test.com&password=pass1234" "$A/signup" | head -10
echo
echo "=== page ==="
curl -s -m 20 -b /tmp/j752.txt -c /tmp/j752.txt "$A/" | grep -iE "logout|expense|report|add|href" | head -15
echo
echo "=== login si besoin ==="
curl -s -m 20 -i -c /tmp/j752.txt -d "username=hacker1&password=pass1234" "$A/login" | head -8
curl -s -m 20 -b /tmp/j752.txt "$A/" | grep -iE "logout|dashboard|expense" | head -8
