#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== un paquet du stream 4 : champs disponibles ==="
tshark -r 311_torrent.pcap -Y "tcp.stream==4" -c 3 2>/dev/null | head -10
echo
echo "=== verbose d'un paquet avec donnees ==="
tshark -r 311_torrent.pcap -Y "tcp.stream==4" -T fields -e frame.number -e tcp.len -e data.len -e _ws.col.Protocol 2>/dev/null | head -8
echo
echo "=== liste des champs data* ==="
tshark -r 311_torrent.pcap -Y "tcp.stream==4" -V -c 1 2>/dev/null | grep -iE "^Data|payload|Protocols in frame" | head -10
