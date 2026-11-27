#!/bin/bash
cd /tmp/winadb
objdump -d -M intel WinAntiDbg0x200.exe > /tmp/d200.asm 2>/dev/null
awk '/^  401f[0-9a-f][0-9a-f]:/,/^  4021b[0-9a-f]:/' /tmp/d200.asm | head -140
