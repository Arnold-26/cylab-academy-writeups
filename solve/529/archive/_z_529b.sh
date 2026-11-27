#!/bin/bash
B="http://chatelaine.cylabacademy.net:48796"
echo "=== accueil ==="
curl -s -m 25 -o /tmp/pb.html -w "HTTP %{http_code} %{size_download}o\n" "$B/"
head -c 1500 /tmp/pb.html
echo
echo "=== liens ==="
grep -oE 'href="[^"]+"|src="[^"]+"' /tmp/pb.html | sort -u | head -20
