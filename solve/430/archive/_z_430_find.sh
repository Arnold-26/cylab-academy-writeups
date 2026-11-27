#!/bin/bash
cd /tmp/winadb
for exe in WinAntiDbg0x200.exe WinAntiDbg0x300.exe; do
  echo "############ $exe"
  objdump -d -M intel "$exe" > /tmp/d.asm 2>/dev/null
  # adresse de la chaine config.bin dans .rdata
  off=$(strings -a -t x "$exe" | grep -m1 "config.bin" | awk '{print $1}')
  echo "chaine config.bin @ file 0x$off -> vaddr 0x$(printf '%x' $((0x$off + 0x400000 - 0x1f?? )) 2>/dev/null)"
  # plus simple : chercher les push d'immediats proches de 0x402xxx referencant la zone rdata
  grep -nE "push +0x40(19|1a|18)[0-9a-f]{2}" /tmp/d.asm | head -5
  echo "--- refs immediates 0x40218/0x40219"
  grep -nE "0x40218[0-9a-f]|0x40219[0-9a-f]|0x4021a[0-9a-f]" /tmp/d.asm | head -8
done
