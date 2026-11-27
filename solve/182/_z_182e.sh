#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cat > /tmp/t182.js <<'EOF'
const fs = require('fs');
const buf = fs.readFileSync('/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/182_wasm.bin');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  console.log('exports:', Object.keys(ex));
  const mem = new Uint8Array(ex.memory.buffer);
  // etat initial de la memoire autour de 0x80 (segment de donnees)
  console.log('data[0..43]:', [...mem.slice(0x80, 0x80+43)].map(x=>x.toString(16).padStart(2,'0')).join(' '));
  // envoyer une entree connue
  const inp = 'picoCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}';
  for (let i = 0; i < inp.length; i++) ex.copy_char(inp.charCodeAt(i), i);
  ex.copy_char(0, inp.length);
  console.log('apres copy_char, mem[0..48]:', [...mem.slice(0, 48)].map(x=>x.toString(16).padStart(2,'0')).join(' '));
  console.log('check_flag =', ex.check_flag());
})();
EOF
node /tmp/t182.js 2>&1 | head -20
