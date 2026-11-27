#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 55_sice_cream 2>/dev/null | grep -B8 "call.*<read@plt>" | head -40
