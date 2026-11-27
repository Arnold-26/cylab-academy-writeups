#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x80eab40 --stop-address=0x80eacc0 171_enter_password 2>/dev/null | head -80
