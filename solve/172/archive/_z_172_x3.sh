#!/bin/bash
cd /tmp/office
for va in 804a0c3 804a130 804a13c 804a145 804a04e; do
  echo "--- $va ---"
  grep -n "$va" asm.txt | head -3
done
