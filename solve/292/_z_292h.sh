#!/bin/bash
cd /tmp/cylab_eps || exit 1
for A in 0x080ab50d 0x0804901e 0x08049a31 0x0805848e 0x08049f12 0x080493fd3; do
  echo "=== $A ==="
  objdump -d -Mintel --start-address=$((A)) --stop-address=$((A+14)) 292_vuln 2>/dev/null | tail -7
done
