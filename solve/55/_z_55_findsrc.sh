#!/bin/bash
cd /mnt/d/ctf-index/_z_55
echo "=== adresse de la chaine (out)"
strings -a -t x libc.so.6 | grep -n "double free or corruption" | head
echo "=== recherche dans le code"
objdump -d libc.so.6 > /tmp/libc.asm 2>/dev/null
grep -c . /tmp/libc.asm
for a in $(strings -a -t x libc.so.6 | grep "double free or corruption (out)" | awk '{print $1}'); do
  echo "offset fichier $a"
done
