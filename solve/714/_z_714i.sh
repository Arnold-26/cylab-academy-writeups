#!/bin/bash
cd /tmp/tl || exit 1
tshark -r rogue_tower.pcap -T fields -e frame.number -e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Info 2>/dev/null | head -30
