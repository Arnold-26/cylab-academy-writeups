#!/bin/bash
P="~/.dsh/attachments/v1/files/43/43be60629ba01766c6880b834d378edabe78a4874cd919efc69631cf32fa932e/torrent.pcap"
echo "=== taille ==="
ls -la "$P" | awk '{print $5}'
echo "=== recherche .iso en clair ==="
strings -n 6 "$P" | grep -ai "\.iso" | head -20
echo "=== recherche .torrent / info / bencode ==="
strings -n 6 "$P" | grep -aiE "\.torrent|announce|info_hash|piece length|utf-8" | head -10
