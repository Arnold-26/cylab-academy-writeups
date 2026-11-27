#!/bin/bash
cd /tmp/c136 || exit 1
cp -f /mnt/d/ctf-index/_z_136_solve.py .
FAKEFLAG='academy{clouds_local_test_flag_1234567890}' timeout 240 python3 -u _z_136_solve.py local "${1:-512}" > /tmp/c136/log.txt 2>&1
echo "exit=$?"
tail -20 /tmp/c136/log.txt
