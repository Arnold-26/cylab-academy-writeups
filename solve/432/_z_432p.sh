#!/bin/bash
cd /tmp/cylab_eps || exit 1
exiftool -v3 432_original.jpg 2>/dev/null | grep -iB3 -A6 "timestamp" | head -40
