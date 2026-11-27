#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/pach/server || exit 1
sed -n '1,68p' index.js
echo "########## Dockerfile ##########"
cat Dockerfile
