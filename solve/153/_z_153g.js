const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/153_qCCYI0ajpD.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const m = new Uint8Array(ex.memory.buffer);
  console.log('globals: key=', ex.key && ex.key.value, 'input addr=', ex.input);
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
  console.log('=== 0x400-0x480 ===');
  dump(0x400, 0x80);
  // essai avec un flag
  const s = 'academy{test}';
  for (let i = 0; i < s.length; i++) ex.copy_char(s.charCodeAt(i), i);
  ex.copy_char(0, s.length);
  const r = ex.check_flag();
  console.log('check_flag ->', r);
  console.log('=== buffer input apres check (0x400) ===');
  dump(0x400, 0x80);
})();
