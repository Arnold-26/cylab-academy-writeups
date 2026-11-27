const fs = require('fs');
const buf = fs.readFileSync('C:/Users/arnol/AppData/Local/Temp/cylab_eps/182_ZoRd23o0wd.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const m = new Uint8Array(ex.memory.buffer);
  const EXPECTED = Array.from(m.slice(0x400, 0x400 + 96));
  const expLen = 41;
  function transformed(str) {
    for (let i = 0; i < str.length; i++) ex.copy_char(str.charCodeAt(i), i);
    ex.copy_char(0, str.length);
    ex.check_flag();
    return Array.from(new Uint8Array(ex.memory.buffer).slice(0x430, 0x430 + 96));
  }
  let flag = 'academy{';
  const alpha = [];
  for (let c = 32; c < 127; c++) alpha.push(String.fromCharCode(c));
  while (flag.length < expLen) {
    let found = null;
    for (const ch of alpha) {
      const cand = flag + ch;
      let tt;
      try { tt = transformed(cand); } catch (e) { continue; }
      if (tt[cand.length - 1] === EXPECTED[cand.length - 1]) { found = ch; break; }
    }
    if (found === null) { console.log('bloque a', flag.length, 'prefixe', flag); break; }
    flag += found;
    console.log('  ', flag);
    if (flag.endsWith('}')) break;
  }
  console.log('FLAG:', flag);
  for (let i = 0; i < flag.length; i++) ex.copy_char(flag.charCodeAt(i), i);
  ex.copy_char(0, flag.length);
  console.log('verification check_flag ->', ex.check_flag());
})();
