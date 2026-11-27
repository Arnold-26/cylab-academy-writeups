#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -j .plt -Mintel 214_horse 2>/dev/null | grep -E '^0+[0-9a-f]+ <|# 601f' | head -40
