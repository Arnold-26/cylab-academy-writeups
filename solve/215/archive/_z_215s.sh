#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x4008a8 --stop-address=0x400905 215_chall 2>/dev/null | tail -30
