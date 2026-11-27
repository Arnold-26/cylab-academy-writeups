#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x1600 --stop-address=0x16c0 151_remote 2>/dev/null | head -80
