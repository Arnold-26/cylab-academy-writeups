#!/bin/bash
cd /tmp/winadb
echo arnold | sudo -S pkill -f "apt-get install" 2>/dev/null
sleep 1
echo "=== r2: analyse 0x300, refs vers config.bin"
timeout 300 r2 -e bin.relocs.apply=true -A -q -c 'izz~config.bin;axt @@ str.*config*' WinAntiDbg0x300.exe 2>/dev/null | head -20
echo "=== r2: liste des fonctions"
timeout 300 r2 -A -q -c 'afl' WinAntiDbg0x300.exe 2>/dev/null | head -40
