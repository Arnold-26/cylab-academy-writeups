#!/bin/bash
set -x
cd ./_z_441
V=2.35-0ubuntu3.3
if [ ! -f ld-2.35.so ]; then
  cd /tmp
  curl -sfO http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/libc6_${V}_amd64.deb || \
  curl -sfO http://security.ubuntu.com/ubuntu/pool/main/g/glibc/libc6_${V}_amd64.deb
  ls -la libc6_${V}_amd64.deb
  rm -rf debx && mkdir -p debx && dpkg-deb -x libc6_${V}_amd64.deb debx
  cp debx/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 ./_z_441/ld-2.35.so
  cp debx/lib/x86_64-linux-gnu/libc.so.6 /tmp/libc_from_deb.so.6
  cd ./_z_441
fi
ls -la
patchelf --set-interpreter ./ld-2.35.so --set-rpath . ./hft
patchelf --print-interpreter ./hft
file ./hft
