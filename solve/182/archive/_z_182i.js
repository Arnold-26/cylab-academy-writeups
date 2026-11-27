const fs = require('fs');
const buf = fs.readFileSync('/tmp/cylab_eps/182_ZoRd23o0wd.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(buf, {});
  const ex = instance.exports;
  const IN = ex.input.value;
  const LEN = 41;
  function run(arr) {
    for (let i = 0; i < arr.length; i++) ex.copy_char(arr.charCodeAt(i), i);
    ex.copy_char(0, arr.length);
    ex.check_flag();
    return Array.from(new Uint8Array(ex.memory.buffer).slice(IN, IN + 64));
  }
  const base = 'academy{' + 'a'.repeat(LEN - 8);
  const ref = run(base);
  console.log('ref:', ref.slice(0, 41).map(b => b.toString(16).padStart(2, '0')).join(' '));
  for (const pos of [0, 1, 2, 8, 9, 40]) {
    const changed = new Set();
    for (const ch of ['z', 'Q', '5', '~']) {
      const cand = base.slice(0, pos) + ch + base.slice(pos + 1);
      const t = run(cand);
      for (let i = 0; i < 41; i++) if (t[i] !== ref[i]) changed.add(i);
    }
    console.log('varier pos', pos, '-> change les sorties:', Array.from(changed).sort((a, b) => a - b).join(','));
  }
})();
