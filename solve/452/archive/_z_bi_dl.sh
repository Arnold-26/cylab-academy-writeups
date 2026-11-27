#!/bin/bash
set -e
rm -rf /tmp/bi && mkdir -p /tmp/bi && cd /tmp/bi
B=https://challenge-files.cylabacademy.net/library
curl -sSL -o bininst1.zip "$B/b707862077450010bce3c050b139b7c00762859eb94eea5db8eded717a6318d0/bininst1.zip"
curl -sSL -o bininst2.zip "$B/ce8f745beda824c87d5482c853c90b7758b9a95d9b05db0c74fb2b0678f8115b/bininst2.zip"
ls -la
echo "=== unzip 1 ==="
mkdir -p b1 && cd b1 && unzip -o -P academy ../bininst1.zip
ls -la
for f in *; do file "$f"; done
cd ..
echo "=== unzip 2 ==="
mkdir -p b2 && cd b2 && unzip -o -P academy ../bininst2.zip
ls -la
for f in *; do file "$f"; done
