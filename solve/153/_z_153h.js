const fs = require('fs');
const buf = fs.readFileSync('C:/Users/arnol/AppData/Local/Temp/cylab_eps/153_qCCYI0ajpD.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const m = new Uint8Array(ex.memory.buffer);
  const EXPECTED = Array.from(m.slice(0x400, 0x400 + 64));
  let expLen = EXPECTED.indexOf(0);
  // la zone attendue peut contenir des zeros internes : on prend jusqu'au premier 0
  if (expLen <= 0) expLen = 43;
  console.log('attendu (%d octets):', expLen, EXPECTED.slice(0, expLen).map(b => b.toString(16)).join(' '));

  function transformed(str) {
    for (let i = 0; i < str.length; i++) ex.copy_char(str.charCodeAt(i), i);
    ex.copy_char(0, str.length);
    ex.check_flag();
    return Array.from(new Uint8Array(ex.memory.buffer).slice(0x430, 0x430 + 64));
  }
  // verification : 'academy{' doit donner les 8 premiers octets attendus
  const t = transformed('academy{');
  console.log('academy{ ->', t.slice(0, 8).map(b => b.toString(16)).join(' '));
  console.log('attendu  ->', EXPECTED.slice(0, 8).map(b => b.toString(16)).join(' '));

  let flag = 'academy{';
  const alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789_{}!ABCDEFGHIJKLMNOPQRSTUVWXYZ-';
  while (flag.length < expLen) {
    let found = null;
    for (const ch of alphabet) {
      const cand = flag + ch;
      const tt = transformed(cand);
      if (tt[cand.length - 1] === EXPECTED[cand.length - 1]) {
        found = ch;
        break;
      }
    }
    if (found === null) { console.log('bloque a', flag.length, 'prefixe', flag); break; }
    flag += found;
    console.log('  ', flag);
    if (flag.endsWith('}')) break;
  }
  console.log('FLAG:', flag);
})();
