#!/bin/bash
U=$(cat ./_z_725url.txt)
echo "URL=$U"
echo "=== pays de l'exit Tor ==="
curl -s -m 40 --socks5-hostname 127.0.0.1:9050 "http://ip-api.com/json/?fields=status,country,countryCode,query" | head -c 300
echo
echo "=== direct (temoin) ==="
curl -s -m 25 -o /tmp/n_direct.txt -w "HTTP %{http_code} %{size_download}o\n" "$U/"
grep -oE "No flag in this region|academy\{[^}]*\}" /tmp/n_direct.txt | head -3
echo "=== via Tor ==="
curl -s -m 60 --socks5-hostname 127.0.0.1:9050 -o /tmp/n_tor.txt -w "HTTP %{http_code} %{size_download}o\n" "$U/"
head -c 600 /tmp/n_tor.txt
echo
grep -oE "academy\{[^}]*\}" /tmp/n_tor.txt | head -3
