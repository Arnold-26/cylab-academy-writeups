#!/bin/bash
P="~/.dsh/attachments/v1/files/43/43be60629ba01766c6880b834d378edabe78a4874cd919efc69631cf32fa932e/torrent.pcap"
echo "=== hierarchie des protocoles (extrait) ==="
timeout 300 tshark -r "$P" -q -z io,phs 2>/dev/null | grep -iE "bittorrent|bt-dht|http|tcp|udp|data" | head -20
echo
echo "=== paquets bittorrent (info) ==="
timeout 300 tshark -r "$P" -Y "bittorrent" -T fields -e frame.number -e _ws.col.Info 2>/dev/null | head -25
