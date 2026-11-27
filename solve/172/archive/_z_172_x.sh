#!/bin/bash
cd /tmp/office
objdump -d -M intel the_office > asm.txt
wc -l asm.txt
echo "=== refs 0x804b2c0 (Address: ...) ==="
grep -n '804b2c0' asm.txt | head -5
echo "=== refs 0x804b207 (Canary) ==="
grep -n '804b207' asm.txt | head -5
echo "=== refs 0x804b239 (Heap bottom) ==="
grep -n '804b239' asm.txt | head -5
