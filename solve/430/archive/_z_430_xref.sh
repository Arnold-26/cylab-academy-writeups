#!/bin/bash
cd /tmp/winadb
echo "=== xref vers la chaine config.bin (vaddr ~0x402190)"
objdump -d -M intel WinAntiDbg0x200.exe > /tmp/wad200.asm 2>/dev/null
grep -n "402190\|40218\|40219" /tmp/wad200.asm | head -10
echo "=== taille du .text"
grep -A3 "text" /tmp/wad200.asm | head -8
echo "=== fonctions contenant des appels a CreateFileA/ReadFile ? (imports)"
objdump -p WinAntiDbg0x200.exe 2>/dev/null | grep -iE "CreateFile|ReadFile|WriteFile|VirtualProtect|RtlAddVectored|AddVectored|SetThreadContext|GetThreadContext|CreateProcess|OpenProcess" | head -20
