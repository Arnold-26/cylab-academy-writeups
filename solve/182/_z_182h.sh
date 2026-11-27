#!/bin/bash
echo arnold | sudo -S apt-get install -y wabt 2>&1 | tail -5
echo "=== wasm2wat ? ==="
which wasm2wat wasm-objdump 2>/dev/null
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
if command -v wasm2wat >/dev/null; then
  wasm2wat 182_wasm.bin -o /tmp/182.wat 2>/dev/null
  wc -l /tmp/182.wat
  echo "=== check_flag ==="
  sed -n '/func \$check_flag/,/^  (func /p' /tmp/182.wat | head -60
fi
