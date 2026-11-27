#!/bin/bash
cd /tmp/tl || exit 1
echo "=== DNS ==="
tshark -r rogue_tower.pcap -Y dns -T fields -e frame.number -e dns.qry.name -e dns.a 2>/dev/null | head -15
echo "=== HTTP requests ==="
tshark -r rogue_tower.pcap -Y http.request -T fields -e frame.number -e http.host -e http.request.uri -e http.user_agent 2>/dev/null | head -15
echo "=== HTTP responses ==="
tshark -r rogue_tower.pcap -Y http.response -T fields -e frame.number -e http.response.code -e http.file_data 2>/dev/null | head -10
echo "=== UDP data ==="
tshark -r rogue_tower.pcap -Y data -T fields -e frame.number -e ip.src -e ip.dst -e data.data 2>/dev/null | head -10
