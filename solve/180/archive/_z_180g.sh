#!/bin/bash
B="http://xebec.cylabacademy.net:38430"
for p in /cookie.phps /authentication.phps /authentication.php; do
  echo "########## $p ##########"
  curl -s -m 15 -o /tmp/x.txt -w "HTTP %{http_code} taille %{size_download}\n" "$B$p"
  head -c 1200 /tmp/x.txt
  echo
done
