#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== payloads TCP (hex+ascii) ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "tcp.len>0" -T fields -e frame.number -e ip.src -e tcp.seq -e tcp.len -e tcp.payload 2>/dev/null | head -30
echo "=== flux suivi ==="
tshark -r 84_shark-on-wire-2-capture.pcap -q -z follow,tcp,ascii,0 2>/dev/null | head -40
