#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 27_investigative-reversing-1-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '30,120p'
