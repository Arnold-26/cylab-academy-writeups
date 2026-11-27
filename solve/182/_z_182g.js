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
  const base = 'academy{' + 'a'.repeat(LEN - 8);
  for (const pos of [1, 9]) {
    const map = {};
    for (let c = 32; c < 127; c++) {
      const cand = base.slice(0, pos) + String.fromCharCode(c) + base.slice(pos + 1);
      const tt = transformed(cand);
      const v = tt[pos];
      (map[v] = map[v] || []).push(String.fromCharCode(c));
    }
    console.log('position', pos, '-> cible', EXPECTED[pos].toString(16));
    const collisions = Object.entries(map).filter(([k, v]) => v.length > 1);
    console.log('  valeurs distinctes:', Object.keys(map).length, '| collisions:', collisions.length);
    console.log('  candidats pour la cible:', (map[EXPECTED[pos]] || []).join(''));
  }
})();
