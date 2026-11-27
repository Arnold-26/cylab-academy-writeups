#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 36_no_auth_mistery 2>/dev/null | sed -n '/<encode>:/,/^$/p' | sed -n '60,120p'
