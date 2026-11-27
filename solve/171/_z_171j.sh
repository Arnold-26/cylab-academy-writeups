#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== local ==="
printf 'reverseengineericanbarelyforward\ngoldfish\n' | timeout 10 ./171_enter_password 2>&1 | head -20
