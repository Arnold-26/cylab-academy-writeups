#!/bin/bash
cd /tmp/winadb
echo "=== symboles ReadConfig / DecryptFlag / FLAG"
timeout 240 r2 -q -c 'idp WinAntiDbg0x300.pdb' -c 'is~ReadConfig' -c 'is~FLAG' WinAntiDbg0x300.exe 2>/dev/null | head -12
echo "=== DecryptFlag"
timeout 240 r2 -q -c 'idp WinAntiDbg0x300.pdb' -c 's 0x402cb0' -c 'pdf' WinAntiDbg0x300.exe 2>/dev/null | head -80
