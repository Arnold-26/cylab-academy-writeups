#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== imp.red ==="
cat 370_imp.red
echo "=== 141 try_me.pcap : protocoles ==="
tshark -r 141_try_me.pcap -q -z io,phs 2>/dev/null | head -20
echo "=== chaines flag ==="
strings -n 6 141_try_me.pcap | grep -aoE "(academy|picoCTF)\{[^}]*\}" | head -5
echo "=== indices ==="
strings -n 8 141_try_me.pcap | grep -aiE "flag|hidden|map|treasure|next|step" | head -15
