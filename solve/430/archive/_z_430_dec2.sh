#!/bin/bash
cd /tmp/winadb
timeout 240 r2 -q -c 'idp WinAntiDbg0x300.pdb' -c 's 0x00402cb0' -c 'pd 70' WinAntiDbg0x300.exe > /tmp/dec300.txt 2>&1
wc -l /tmp/dec300.txt
cat /tmp/dec300.txt
