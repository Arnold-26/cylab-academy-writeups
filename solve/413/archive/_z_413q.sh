#!/bin/bash
SRC="/tmp/cylab_eps/413_full.img.gz"
ls -la "$SRC"
echo "=== integrite ==="
gzip -t "$SRC" 2>&1 && echo "GZ OK" || echo "GZ INCOMPLET"
echo "=== decompression si OK ==="
if gzip -t "$SRC" 2>/dev/null; then
  cd /tmp || exit 1
  gunzip -c "$SRC" > t413full.img
  ls -la t413full.img
  file t413full.img | cut -c1-160
fi
