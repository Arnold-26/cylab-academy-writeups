// 478 Pachinko — find the real primary inputs of the netlist.
// Test: baseline all-zero; then set exactly one index to 255 and re-run.
// If state[i] survives as 255, no gate writes bit i => i is a primary input (or unused).
// If the run differs elsewhere too, bit i actually feeds logic.
const W = 'D:\\ctf-index\\_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const fs = require('fs');
const N = 100000;
const LIMIT = 6000;

const base = new Uint8Array(N);
wasmProcess(base);
const baseCopy = Uint8Array.from(base);

const rows = [];
for (let i = 0; i < LIMIT; i++) {
  const s = new Uint8Array(N);
  s[i] = 255;
  wasmProcess(s);
  const survives = s[i] === 255;
  let diff = 0;
  let firstDiffs = [];
  for (let j = 0; j < LIMIT; j++) {
    if (s[j] !== baseCopy[j]) { diff++; if (firstDiffs.length < 6) firstDiffs.push(j); }
  }
  rows.push({ i, survives, diff, firstDiffs });
}
const survivors = rows.filter(r => r.survives);
const inputs = survivors.filter(r => r.diff > 0);
fs.writeFileSync('D:\\ctf-index\\_z_pachinko\\_z_rev_inputs.json', JSON.stringify({ rows, survivors, inputs }, null, 0));
console.log('tested', LIMIT);
console.log('survivors (not overwritten):', survivors.length);
console.log('of which affect logic:', inputs.length);
console.log(JSON.stringify(inputs.map(r => [r.i, r.diff])));
