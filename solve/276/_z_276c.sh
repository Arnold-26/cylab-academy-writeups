#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 276_keygenme 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -80
