#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
if [ ! -s 494_server.tar.gz ]; then
  curl -s -m 120 -o 494_server.tar.gz "https://challenge-files.cylabacademy.net/library/05811f9f3ba7253920faabd5a8b2308ee44ade0e89a016380957f654cb168262/server.tar.gz"
fi
ls -la 494_server.tar.gz
rm -rf pach && mkdir -p pach && cd pach || exit 1
tar xzf ../494_server.tar.gz 2>/dev/null
find . -type f | head -25
