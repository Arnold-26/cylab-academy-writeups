#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
mkdir -p o141 && rm -f o141/*
echo "=== objets HTTP ==="
timeout 300 tshark -r 141_try_me.pcap --export-objects http,o141 -q 2>/dev/null
ls -la o141/ | head -20
echo "=== requetes HTTP ==="
timeout 200 tshark -r 141_try_me.pcap -Y "http.request" -T fields -e frame.number -e http.request.method -e http.host -e http.request.uri 2>/dev/null | head -10
echo "=== reponses ==="
timeout 200 tshark -r 141_try_me.pcap -Y "http.response" -T fields -e frame.number -e http.response.code -e http.content_type -e http.content_length 2>/dev/null | head -10
