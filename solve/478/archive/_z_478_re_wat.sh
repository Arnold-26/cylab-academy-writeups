#!/bin/bash
set -e
cd /tmp
wasm2wat --no-check ./_z_pachinko/server/wasm/pkg/verilog_ctf_wasm_bg.wasm -o cpu.wat
ls -la cpu.wat
echo "store8 count: $(grep -c 'i32.store8' cpu.wat)"
echo "load8_u count: $(grep -c 'i32.load8_u' cpu.wat)"
grep -n 'export "process"' cpu.wat || true
