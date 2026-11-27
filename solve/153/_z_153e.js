const fs = require('fs');
const buf = fs.readFileSync('C:/Users/arnol/AppData/Local/Temp/cylab_eps/153_qCCYI0ajpD.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  console.log('exports:', Object.keys(ex));
  if (ex.memory) {
    const m = new Uint8Array(ex.memory.buffer);
    console.log('memoire:', m.length, 'octets');
    // dump non nul
    let s = '';
    for (let i = 0; i < Math.min(m.length, 4096); i++) {
      s += (m[i] >= 32 && m[i] < 127) ? String.fromCharCode(m[i]) : '.';
      if (i % 64 === 63) { console.log(i - 63, s); s = ''; }
    }
  }
})();
