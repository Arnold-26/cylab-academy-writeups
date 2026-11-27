#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== flux portant des donnees ==="
tshark -r 311_torrent.pcap -Y "tcp.len>0" -T fields -e tcp.stream -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.len 2>/dev/null | sort -u | head -25
