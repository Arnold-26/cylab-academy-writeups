#!/bin/bash
A="http://chatelaine.cylabacademy.net:12271"
echo "=== accueil ==="
curl -s -m 20 -i "$A/" | head -30
