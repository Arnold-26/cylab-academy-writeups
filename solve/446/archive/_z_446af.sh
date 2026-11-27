#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x804991f --stop-address=0x8049a24 446_game 2>/dev/null | tail -50
