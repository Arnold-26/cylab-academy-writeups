#!/bin/bash
cd /tmp/winadb
echo "=== upx dispo ?"
command -v upx || command -v upx-ucl || apt list --installed 2>/dev/null | grep -i upx
echo "=== tentative de deupx"
cp WinAntiDbg0x300.exe u300.exe
(upx -d u300.exe 2>&1 || upx-ucl -d u300.exe 2>&1) | tail -8
ls -la u300.exe WinAntiDbg0x300.exe
rabin2 -S u300.exe 2>/dev/null | head -10
