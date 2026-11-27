#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x1420 --stop-address=0x14e0 276_keygenme 2>/dev/null | tail -40
