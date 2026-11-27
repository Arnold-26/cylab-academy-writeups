#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x400a4d --stop-address=0x400c62 75_zero_to_hero 2>/dev/null | grep -E "call|lea|sub +rsp|read|rep" | head -40
