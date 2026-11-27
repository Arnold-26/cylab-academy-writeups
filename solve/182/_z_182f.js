const fs = require('fs');
const buf = fs.readFileSync('C:/Users/arnol/AppData/Local/Temp/cylab_eps/182_ZoRd23o0wd.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const m = new Uint8Array(ex.memory.buffer);
  const EXPECTED = Array.from(m.slice(0x400, 0x400 + 96));
  const LEN = 41;
  function transformed(arr) {
    for (let i = 0; i < arr.length; i++) ex.copy_char(arr.charCodeAt(i), i);
    ex.copy_char(0, arr.length);
    ex.check_flag();
    return Array.from(new Uint8Array(ex.memory.buffer).slice(0x430, 0x430 + 96));
  }
  const alpha = [];
  for (let c = 32; c < 127; c++) alpha.push(String.fromCharCode(c));
  let cur = 'academy{' + 'a'.repeat(LEN - 8);
  // verifie les 8 premiers
  let t = transformed(cur);
  console.log('base:', t.slice(0, 8).map(b => b.toString(16)).join(' '), '| attendu', EXPECTED.slice(0, 8).map(b => b.toString(16)).join(' '));
  for (let i = 0; i < LEN; i++) {
    let found = null;
    for (const ch of alpha) {
      const cand = cur.slice(0, i) + ch + cur.slice(i + 1);
      const tt = transformed(cand);
      if (tt[i] === EXPECTED[i]) { found = ch; break; }
    }
    if (found === null) { console.log('bloque a', i, 'prefixe', cur); break; }
    cur = cur.slice(0, i) + found + cur.slice(i + 1);
    console.log('  [%d] %s', i, cur);
    if (cur.endsWith('}')) break;
  }
  console.log('RESULTAT:', cur);
  for (let i = 0; i < cur.length; i++) ex.copy_char(cur.charCodeAt(i), i);
  ex.copy_char(0, cur.length);
  console.log('check_flag ->', ex.check_flag());
})();
