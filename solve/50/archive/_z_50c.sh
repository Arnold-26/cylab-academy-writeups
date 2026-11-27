#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 50_seed_spring 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -70
