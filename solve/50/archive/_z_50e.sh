#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x13bb --stop-address=0x14c0 50_seed_spring 2>/dev/null | tail -60
