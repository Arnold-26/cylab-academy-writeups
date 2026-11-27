#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
echo "### whoami: $(whoami)"
echo "### step1 update"
apt-get update -qq 2>&1 | tail -3
echo "### step2 install lld"
apt-get install -y -qq lld 2>&1 | tail -5
echo "### step3 verify"
if command -v ld.lld >/dev/null 2>&1; then echo "OK ld.lld: $(ld.lld --version 2>&1 | head -1)"; else echo "MISSING ld.lld"; fi
ls /usr/lib/llvm-*/bin/ld.lld 2>/dev/null
ls /usr/bin/*lld* 2>/dev/null
