#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== appels alarm/signal ==="
objdump -d -Mintel 39_need-for-speed 2>/dev/null | grep -B4 -A2 "call.*<alarm@plt>\|call.*<__sysv_signal" | head -25
