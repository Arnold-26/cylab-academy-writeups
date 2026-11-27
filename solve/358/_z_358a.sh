#!/bin/bash
B="http://chatelaine.cylabacademy.net:18689"
echo "=== page d'accueil ==="
curl -s -m 20 "$B/" | head -40
