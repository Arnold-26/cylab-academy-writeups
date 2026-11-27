#!/bin/bash
cd /tmp/cw || exit 1
echo "=== 1 ronde ==="
timeout 60 /usr/games/pmars -r 1 herem.red imp.red 2>&1 | tail -12
echo "=== 10 rondes ==="
timeout 120 /usr/games/pmars -r 10 herem.red imp.red 2>&1 | tail -12
