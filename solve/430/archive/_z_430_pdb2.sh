#!/bin/bash
cd /tmp/winadb
echo "=== r2 + PDB (idp)"
timeout 240 r2 -q -c 'idp WinAntiDbg0x300.pdb' -c 'is~Decrypt' -c 'is~ReadConfig' -c 'f~Decrypt' WinAntiDbg0x300.exe 2>&1 | head -20
echo "=== recherche du symbole dans la table PDB (adresses)"
strings -a -t x WinAntiDbg0x300.pdb | grep -E "DecryptFlag|ReadConfig" | head -5
