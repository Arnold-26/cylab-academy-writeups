#!/bin/bash
cd /tmp/tl || exit 1
echo "=== protocoles ==="
tshark -r rogue_tower.pcap -q -z io,phs 2>/dev/null | head -25
echo "=== strings flag ==="
strings -n 4 rogue_tower.pcap | grep -aoE 'academy\{[^}]*\}|picoCTF\{[^}]*\}' | head -3
echo "=== strings generales ==="
strings -n 5 rogue_tower.pcap | head -20
