#!/bin/bash
B="http://xebec.cylabacademy.net:38430"
for p in /admin.phps /index.phps /cookie.phps /authentication.phps /admin.php /flag; do
  echo "=== $p ==="
  curl -s -m 15 -o /tmp/o.txt -w "%{http_code} %{size_download}\n" "$B$p"
  head -c 900 /tmp/o.txt
  echo
done
