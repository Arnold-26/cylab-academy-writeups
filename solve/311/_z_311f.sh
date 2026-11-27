#!/bin/bash
P="/mnt/c/Users/arnol/.dsh/attachments/v1/files/43/43be60629ba01766c6880b834d378edabe78a4874cd919efc69631cf32fa932e/torrent.pcap"
timeout 600 tshark -r "$P" -Y "bt-dht" -T fields -e frame.number -e _ws.col.Info -e ip.src -e ip.dst > /tmp/dht_full.txt 2>/dev/null
wc -l /tmp/dht_full.txt
echo "=== info_hash distincts ==="
grep -oE "Info_hash=[0-9a-f]+" /tmp/dht_full.txt | sort | uniq -c | sort -rn
echo "=== announce_peer (avec IP source) ==="
grep -i "announce_peer" /tmp/dht_full.txt
echo "=== get_peers (avec IP source) ==="
grep -i "get_peers" /tmp/dht_full.txt
echo "=== IP locales les plus actives ==="
awk -F'\t' '{print $3}' /tmp/dht_full.txt | sort | uniq -c | sort -rn | head -6
