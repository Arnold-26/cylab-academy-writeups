#!/bin/bash
cd /tmp/cylab_eps/pach/server || exit 1
echo "########## index.js ##########"
cat -n index.js
echo
echo "########## cpu.js (debut) ##########"
head -60 cpu.js
