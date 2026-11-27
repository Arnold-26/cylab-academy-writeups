#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/t182c.js <<'EOF'
const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/182_wasm.bin');
let mem = null;
function readStr(ptr) {
  const out = [];
  for (let i = ptr; i < ptr + 200; i++) { const b = mem[i]; if (b === 0) break; out.push(b); }
  return out;
}
function strcmp(a, b) {
  const sa = readStr(a), sb = readStr(b);
  console.log('--- strcmp ---');
  console.log('  a:', sa.map(x=>x.toString(16).padStart(2,'0')).join(' '), '|', String.fromCharCode(...sa));
  console.log('  b:', sb.map(x=>x.toString(16).padStart(2,'0')).join(' '), '|', String.fromCharCode(...sb));
  return 1;
}
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, { env: { strcmp } });
  const ex = instance.exports;
  mem = new Uint8Array(ex.memory.buffer);
  const inp = 'picoCTF{ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789}';
  for (let i = 0; i < inp.length; i++) ex.copy_char(inp.charCodeAt(i), i);
  ex.copy_char(0, inp.length);
  console.log('check_flag =', ex.check_flag());
})();
EOF
node /tmp/t182c.js 2>&1 | head -20
