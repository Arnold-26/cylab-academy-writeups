#!/bin/bash
cd /tmp/cylab_eps || exit 1
for pfx in "academy{" "picoCTF{"; do
  p="${pfx}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}"
  echo "--- $pfx (${#p} caracteres) ---"
  timeout 5 ./149_checkpass "$p" 2>&1 | head -3
done
