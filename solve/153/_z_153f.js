const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/153_qCCYI0ajpD.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  console.log('exports:', Object.keys(ex).join(', '));
  if (ex.memory) {
    const m = new Uint8Array(ex.memory.buffer);
    console.log('memoire:', m.length);
    let nz = [];
    for (let i = 0; i < m.length; i++) if (m[i] !== 0) { nz.push(i); if (nz.length > 40) break; }
    console.log('premiers octets non nuls a:', nz.slice(0, 40).join(','));
    const show = (a) => { let s=''; for (let i=a;i<a+64 && i<m.length;i++) s += (m[i]>=32&&m[i]<127)?String.fromCharCode(m[i]):'.'; console.log(a, s); };
    for (const a of [0, 64, 128, 1024, 2048]) show(a);
  }
  // essai : envoyer un flag factice
  if (ex.copy_char && ex.check_flag) {
    const s = 'academy{test}';
    for (let i = 0; i < s.length; i++) ex.copy_char(s.charCodeAt(i), i);
    ex.copy_char(0, s.length);
    console.log('check_flag ->', ex.check_flag());
  }
})();
