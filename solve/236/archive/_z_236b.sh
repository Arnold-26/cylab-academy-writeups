#!/bin/bash
curl -s -m 20 -i "http://chatelaine.cylabacademy.net:40158/" 2>/dev/null | head -3
echo "=== page JAuth (port inconnu, on relit la desc via API) ==="
