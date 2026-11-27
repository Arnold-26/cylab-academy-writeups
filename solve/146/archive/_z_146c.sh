#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 146_heapedit 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '80,160p'
