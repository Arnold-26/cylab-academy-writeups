const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/182_ZoRd23o0wd.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  console.log('input addr =', ex.input.value);
  const dump = (a, n, label) => {
    const m = new Uint8Array(ex.memory.buffer);
    console.log('---', label, 'a=0x' + a.toString(16));
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
  dump(ex.input.value, 0x40, 'input avant');
  const s = 'academy{';
  for (let i = 0; i < s.length; i++) ex.copy_char(s.charCodeAt(i), i);
  ex.copy_char(0, s.length);
  dump(ex.input.value, 0x40, 'input apres copy_char (avant check)');
  const r = ex.check_flag();
  console.log('check_flag ->', r);
  dump(ex.input.value, 0x40, 'input apres check');
  dump(0x400, 0x40, '0x400 apres check');
})();
