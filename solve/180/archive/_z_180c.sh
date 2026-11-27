#!/bin/bash
cat /tmp/host180.txt 2>/dev/null
H=$(cut -d' ' -f1 /tmp/host180.txt)
P=$(cut -d' ' -f2 /tmp/host180.txt)
echo "--- test ${H}:${P} ---"
curl -s -m 15 -i "http://${H}:${P}/robots.txt" | head -20
echo
echo "--- index ---"
curl -s -m 15 "http://${H}:${P}/" | head -30
