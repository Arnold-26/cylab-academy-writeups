#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -R 215_chall 2>/dev/null
