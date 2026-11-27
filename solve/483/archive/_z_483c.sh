#!/bin/bash
cd /tmp/cylab_eps/y483 || exit 1
which upx || (echo userd | sudo -S apt-get install -y -qq upx-ucl 2>&1 | tail -2; which upx)
if which upx >/dev/null 2>&1; then
  cp suspicious.exe un.exe
  upx -d un.exe 2>&1 | tail -4
  echo "=== strings apres unpack ==="
  strings -n 5 un.exe | grep -aiE "academy|picoCTF|flag|powershell|http|cmd|CreateFile|WriteFile|VirtualAlloc|LoadLibrary" | head -25
else
  echo "upx absent"
fi
