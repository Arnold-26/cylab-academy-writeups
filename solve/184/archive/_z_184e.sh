#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 184_fun 2>/dev/null | sed -n '/<execute>:/,/^$/p' | sed -n '50,120p'
