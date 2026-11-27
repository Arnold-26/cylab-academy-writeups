#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
echo "=== 752 accueil ==="
curl -s -m 20 "$A/" | head -40
echo
echo "=== 729 accueil ==="
curl -s -m 20 "http://xebec.cylabacademy.net:44712/" | grep -iE "<form|input|button|action|script" | head -12
