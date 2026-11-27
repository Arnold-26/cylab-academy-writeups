#!/bin/bash
cd /tmp/cylab_eps/pachinko/server || exit 1
which node npm 2>/dev/null
node --version 2>/dev/null
echo "=== structure wasm/pkg ==="
ls -la wasm/pkg/ | head -10
echo "=== test direct du wasm ==="
cat > /tmp/t494.js <<'EOF'
const { process } = require('/tmp/cylab_eps/pachinko/server/wasm/pkg/verilog_ctf_wasm.js');
const state = new Uint8Array(100000);
for (let i = 0; i < 3; i++) { process(state); }
console.log('wasm ok, premiers octets non nuls:', [...state.slice(0,20)]);
EOF
node /tmp/t494.js 2>&1 | head -10
