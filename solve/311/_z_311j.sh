#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
tshark -r 311_torrent.pcap -Y "tcp.stream==4 && tcp.len>0" -T fields -e tcp.payload 2>/dev/null | tr -d '\n' | xxd -r -p > /tmp/s4.bin 2>/dev/null
ls -la /tmp/s4.bin
echo "=== chaines ==="
strings -n 4 /tmp/s4.bin | head -50
echo
echo "=== bencode : cles ==="
strings -n 3 /tmp/s4.bin | grep -E "name|info|files|path|length|piece|ut_metadata|md" | head -25
