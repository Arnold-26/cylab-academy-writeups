#!/bin/bash
cd /tmp/winadb
echo "=== chaines (toutes, longueur>3)"
strings -a -t x WinAntiDbg0x200.exe | awk 'length($0)>12' | head -40
echo "=== imports"
objdump -p WinAntiDbg0x200.exe 2>/dev/null | sed -n '/DLL Name/,$p' | head -40
