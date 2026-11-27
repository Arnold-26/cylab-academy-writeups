#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/t182k.js <<'EOF'
const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/182_wasm.bin');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const mem = new Uint8Array(ex.memory.buffer);
  const DATA = 1024, INPUT = 1072;
  const orig = Uint8Array.from(mem.slice(DATA, DATA + 64));
  function tryInput(s) {
    mem.fill(0, INPUT, INPUT + 128);
    for (let i = 0; i < s.length; i++) ex.copy_char(s.charCodeAt(i), i);
    ex.copy_char(0, s.length);
    return ex.check_flag();
  }
  // forcer la cible a un seul octet b et trouver quel caractere d'entree passe
  const results = {};
  for (const b of [0x41, 0x42, 0x30, 0x61]) {
    mem.set(orig);
    mem[DATA] = b; mem[DATA + 1] = 0;
    let found = [];
    for (let c = 1; c < 128; c++) {
      if (tryInput(String.fromCharCode(c))) found.push(c);
    }
    console.log('cible', b.toString(16), '-> caracteres acceptes:', found.map(x=>x.toString(16)));
    results[b] = found;
  }
  // deduction de K : cible = char ^ K
  const ks = Object.entries(results).map(([b, arr]) => [Number(b), arr.map(c => (Number(b) ^ c) )]);
  console.log('cles candidates:', JSON.stringify(ks));
})();
EOF
node /tmp/t182k.js 2>&1 | tail -12
