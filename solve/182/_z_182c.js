const fs = require('fs');
const buf = fs.readFileSync('C:/Users/arnol/AppData/Local/Temp/cylab_eps/182_ZoRd23o0wd.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  console.log('exports:', Object.keys(ex).join(', '));
  const m = new Uint8Array(ex.memory.buffer);
  console.log('memoire:', m.length);
  const dump = (a, n) => {
    for (let i = a; i < a + n; i += 16) {
      let hex = [], asc = '';
      for (let j = 0; j < 16 && i + j < a + n; j++) {
        const v = m[i + j];
        hex.push(v.toString(16).padStart(2, '0'));
        asc += (v >= 32 && v < 127) ? String.fromCharCode(v) : '.';
      }
      console.log(i.toString(16).padStart(5, '0'), hex.join(' '), asc);
    }
  };
  console.log('=== 0x400-0x4c0 (avant) ===');
  dump(0x400, 0xc0);
  const s = 'academy{';
  if (ex.copy_char && ex.check_flag) {
    for (let i = 0; i < s.length; i++) ex.copy_char(s.charCodeAt(i), i);
    ex.copy_char(0, s.length);
    console.log('check_flag ->', ex.check_flag());
    console.log('=== apres ===');
    dump(0x400, 0xc0);
  } else {
    console.log('pas de copy_char/check_flag');
  }
})();
