#!/bin/bash
A="http://chatelaine.cylabacademy.net:12271"
echo "=== GET / ==="
curl -s -m 25 -o /tmp/a1.txt -w "HTTP %{http_code} %{size_download}o\n" "$A/"
head -c 600 /tmp/a1.txt
echo
echo "=== impossibleLogin.php~ ==="
curl -s -m 25 -o /tmp/a2.txt -w "HTTP %{http_code} %{size_download}o\n" "$A/impossibleLogin.php~"
cat /tmp/a2.txt
