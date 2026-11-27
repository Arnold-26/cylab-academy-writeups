#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x80496de --stop-address=0x80497bc 446_game 2>/dev/null | tail -40
