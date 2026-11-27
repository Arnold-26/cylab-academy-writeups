#!/bin/bash
cd /tmp/tl || exit 1
echo "=== corps des POST /upload ==="
tshark -r rogue_tower.pcap -Y 'http.request.method=="POST"' -T fields -e frame.number -e http.file_data 2>/dev/null | head -10
echo "=== suivi du stream de 10.100.0.25 ==="
S=$(tshark -r rogue_tower.pcap -Y 'ip.src==10.100.0.25 && tcp' -T fields -e tcp.stream 2>/dev/null | head -1)
echo "stream: $S"
tshark -r rogue_tower.pcap -q -z follow,tcp,ascii,$S 2>/dev/null | head -40
