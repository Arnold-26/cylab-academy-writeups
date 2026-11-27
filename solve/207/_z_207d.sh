#!/bin/bash
cd /tmp/cylab_eps || exit 1
for C in 207 211; do
  echo "=== $C ==="
  openssl rsa -in pm_$C/private.key -check -noout 2>&1 | head -8
  echo "--- asn1parse ---"
  openssl asn1parse -in pm_$C/private.key 2>&1 | head -12
done
