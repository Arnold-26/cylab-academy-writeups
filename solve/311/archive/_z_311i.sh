#!/bin/bash
cd /tmp/cylab_eps || exit 1
tshark -r 311_torrent.pcap -q -z follow,tcp,raw,4 2>/dev/null > /tmp/s4.txt
wc -l /tmp/s4.txt
# reconstituer les octets : les lignes du follow contiennent l'hexa
tail -n +2 /tmp/s4.txt | tr -d ' \t\n' | xxd -r -p > /tmp/s4.bin 2>/dev/null
ls -la /tmp/s4.bin
echo "=== chaines lisibles ==="
strings -n 4 /tmp/s4.bin | head -40
echo
echo "=== recherche des cles bencode ==="
strings -n 3 /tmp/s4.bin | grep -E "^(name|name\.utf-8|info|files|path|length|piece)" | head -20
