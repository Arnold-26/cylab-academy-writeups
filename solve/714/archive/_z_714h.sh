#!/bin/bash
cd /tmp/tl || exit 1
echo "=== streams tcp ==="
tshark -r rogue_tower.pcap -T fields -e tcp.stream 2>/dev/null | sort -u | tr '\n' ' '
echo
for s in 0 1 2 3; do
  echo "--- stream $s ---"
  tshark -r rogue_tower.pcap -q -z follow,tcp,ascii,$s 2>/dev/null | head -25
done
