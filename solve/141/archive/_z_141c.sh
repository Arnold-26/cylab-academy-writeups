#!/bin/bash
cd /tmp/cylab_hid || exit 1
S=$(tshark -r 141_try_me.pcap -Y 'http.host contains "powershell"' -T fields -e tcp.stream 2>/dev/null | head -1)
echo "stream: $S"
tshark -r 141_try_me.pcap -q -z follow,tcp,ascii,$S 2>/dev/null | head -60
