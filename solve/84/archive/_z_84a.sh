#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== protocoles ==="
tshark -r 84_shark-on-wire-2-capture.pcap -q -z io,phs 2>/dev/null | head -12
echo "=== paquets UDP : payload + champs ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "udp" -T fields -e frame.number -e ip.id -e udp.srcport -e udp.dstport -e data.data 2>/dev/null | head -20
echo "=== nombre de paquets UDP ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "udp" 2>/dev/null | wc -l
echo "=== paquets TCP ==="
tshark -r 84_shark-on-wire-2-capture.pcap -Y "tcp" 2>/dev/null | wc -l
