#!/bin/bash
set -x
ls /usr/lib/llvm-*/bin/ld.lld 2>/dev/null
command -v ld.lld || echo "NO ld.lld in PATH"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq 2>&1 | tail -2
apt-get install -y -qq lld llvm 2>&1 | tail -5
command -v ld.lld && ld.lld --version
ls /usr/lib/llvm-21/bin/ | head -50
