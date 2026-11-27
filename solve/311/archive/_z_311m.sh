#!/bin/bash
cd /tmp/cylab_eps || exit 1
tshark -r 311_torrent.pcap -Y "tcp.stream==4" -w /tmp/s4.pcap 2>/dev/null
ls -la /tmp/s4.pcap
echo "=== strings sur le pcap filtre ==="
strings -n 5 /tmp/s4.pcap | grep -avE "^[[:punct:][:space:]]*$" | head -40
echo
echo "=== bencode ==="
strings -n 3 /tmp/s4.pcap | grep -aE "4:name|11:ut_metadata|5:files|4:path|6:length|4:info" | head -20
