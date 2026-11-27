#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== UDP data frames (extrait) ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "udp.length>0" -T fields -e frame.number -e ip.src -e udp.srcport -e udp.dstport -e data.data 2>/dev/null | head -25
echo "=== longueurs de trame des paquets TCP portant des donnees ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "tcp.len>0 && ip.src==192.168.2.1" -T fields -e frame.len -e tcp.payload 2>/dev/null | head -20
echo "=== recherche de texte ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "tcp contains \"pico\"" -T fields -e frame.number 2>/dev/null | head -5
strings -n 8 84_shark-on-wire-2-capture.pcap | grep -iE 'pico|academy|flag' | head -5
