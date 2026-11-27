#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cat > /tmp/t182solver.js <<'EOF'
const fs = require('fs');
const buf = fs.readFileSync('/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/182_wasm.bin');
const CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}-!?#';
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const mem = new Uint8Array(ex.memory.buffer);
  const DATA = 1024, INPUT = 1072;
  const orig = Uint8Array.from(mem.slice(DATA, DATA + 64));
  console.log('data:', [...orig.slice(0,8)].map(x=>x.toString(16)).join(' '));

  function tryInput(s) {
    mem.fill(0, INPUT, INPUT + 128);
    for (let i = 0; i < s.length; i++) ex.copy_char(s.charCodeAt(i), i);
    ex.copy_char(0, s.length);
    return ex.check_flag();
  }
  // oracle : tronquer la cible a k octets -> compare seulement le prefixe
  function prefixOk(cand, k) {
    mem[DATA + k] = 0;
    const r = tryInput(cand);
    mem.set(orig);           // restaurer
    return r === 1;
  }
  console.log('sanity: prefixe vide accepte ?', prefixOk('', 0));

  let known = '';
  for (let k = 0; k < 48; k++) {
    let found = null;
    for (const ch of CHARS) {
      if (prefixOk(known + ch, k + 1)) { found = ch; break; }
    }
    if (!found) { console.log('stop a', k, 'known=', JSON.stringify(known)); break; }
    known += found;
    console.log('k=%2d -> %j   %j', k, found, known);
    if (found === '}') break;
  }
  console.log('RESULTAT:', known);
})();
EOF
node /tmp/t182solver.js 2>&1 | tail -50
