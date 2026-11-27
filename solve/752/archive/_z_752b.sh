#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
echo "=== signup (champs) ==="
curl -s -m 20 "$A/signup" | grep -iE "<form|input|button|action" | head -12
echo
echo "=== inscription ==="
curl -s -m 20 -i -c /tmp/j752.txt -d "username=hacker1&password=pass1234&confirm_password=pass1234" "$A/signup" | head -12
echo
echo "=== page connectee ==="
curl -s -m 20 -b /tmp/j752.txt "$A/" | grep -iE "logout|expense|report|flag|href" | head -15
