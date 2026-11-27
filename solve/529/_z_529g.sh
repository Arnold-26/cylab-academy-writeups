#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
U="http://chatelaine.cylabacademy.net:48796/download/pico-bank.apk"
echo "=== HEAD ==="
curl -s -I -m 30 "$U" | head -10
echo "=== GET verbeux (extrait) ==="
curl -m 60 -o /tmp/t.apk "$U" 2>&1 | tail -12
ls -la /tmp/t.apk 2>/dev/null
echo "=== avec Range sur 1 Mo ==="
curl -s -m 60 -H "Range: bytes=0-1048575" -o /tmp/part.apk -w "HTTP %{http_code} %{size_download}o\n" "$U"
ls -la /tmp/part.apk 2>/dev/null
