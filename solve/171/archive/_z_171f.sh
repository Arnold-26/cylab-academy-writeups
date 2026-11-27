#!/bin/bash
cd /tmp/cylab_eps || exit 1
printf 'reverseengineericanbarelyforward\nabc\n' | timeout 10 ./171_enter_password 2>&1 | head -20
echo "=== symboles main ==="
go tool nm 171_enter_password 2>/dev/null | grep -E " main\." 
echo "=== desassemblage main.main ==="
objdump -d -Mintel --start-address=0x80ea800 --stop-address=0x80eab40 171_enter_password 2>/dev/null | grep -E "call|lea|mov +DWORD PTR \[esp" | head -30
