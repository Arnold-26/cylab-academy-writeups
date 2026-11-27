#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x8049905 --stop-address=0x8049975 446_game 2>/dev/null | tail -45
