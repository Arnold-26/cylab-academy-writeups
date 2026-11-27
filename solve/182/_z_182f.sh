#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cat > /tmp/t182b.js <<'EOF'
const fs = require('fs');
const buf = fs.readFileSync('/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/182_wasm.bin');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const mem = new Uint8Array(ex.memory.buffer);
  const hex = a => [...a].map(x=>x.toString(16).padStart(2,'0')).join(' ');
  const asc = a => [...a].map(x=> (x>=32&&x<127)?String.fromCharCode(x):'.').join('');
  console.log('data @0x400 :', hex(mem.slice(0x400, 0x400+43)));
  console.log('data ascii  :', asc(mem.slice(0x400, 0x400+43)));
  console.log('input ptr   :', ex.input);
  console.log('zone 0x600-0x680:', asc(mem.slice(0x600, 0x680)));
  // ecrire des caracteres
  for (let i = 0; i < 5; i++) ex.copy_char(0x41 + i, i);
  ex.copy_char(0, 5);
  console.log('apres copy_char(ABCDE) @input:', hex(mem.slice(ex.input, ex.input+8)), asc(mem.slice(ex.input, ex.input+8)));
  console.log('check_flag:', ex.check_flag());
})();
EOF
node /tmp/t182b.js 2>&1 | head -20
