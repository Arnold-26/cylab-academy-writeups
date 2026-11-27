#!/bin/bash
P="/mnt/c/Users/arnol/.dsh/attachments/v1/files/43/43be60629ba01766c6880b834d378edabe78a4874cd919efc69631cf32fa932e/torrent.pcap"
timeout 600 tshark -r "$P" -Y "bt-dht" -T fields -e frame.number -e _ws.col.Info > /tmp/dht_info.txt 2>/dev/null
wc -l /tmp/dht_info.txt
head -40 /tmp/dht_info.txt
