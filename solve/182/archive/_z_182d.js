const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/182_ZoRd23o0wd.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  let m = new Uint8Array(ex.memory.buffer);
  const EXPECTED = Array.from(m.slice(0x400, 0x400 + 96));
  let expLen = EXPECTED.indexOf(0);
  if (expLen <= 0) expLen = 35;
  console.log('attendu (%d):', expLen, EXPECTED.slice(0, expLen).map(b => b.toString(16)).join(' '));
  function transformed(str) {
    for (let i = 0; i < str.length; i++) ex.copy_char(str.charCodeAt(i), i);
    ex.copy_char(0, str.length);
    ex.check_flag();
    return Array.from(new Uint8Array(ex.memory.buffer).slice(0x430, 0x430 + 96));
  }
  const t = transformed('academy{');
  console.log('academy{ ->', t.slice(0, 8).map(b => b.toString(16)).join(' '));
  let flag = 'academy{';
  const alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789_{}!ABCDEFGHIJKLMNOPQRSTUVWXYZ-';
  while (flag.length < expLen) {
    let found = null;
    for (const ch of alphabet) {
      const cand = flag + ch;
      const tt = transformed(cand);
      if (tt[cand.length - 1] === EXPECTED[cand.length - 1]) { found = ch; break; }
    }
    if (found === null) { console.log('bloque a', flag.length, flag); break; }
    flag += found;
    if (flag.endsWith('}')) break;
  }
  console.log('FLAG:', flag);
  // verification finale
  for (let i = 0; i < flag.length; i++) ex.copy_char(flag.charCodeAt(i), i);
  ex.copy_char(0, flag.length);
  console.log('check_flag final ->', ex.check_flag());
})();
