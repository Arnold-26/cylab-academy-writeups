// 478 Pachinko — find the clock bit: toggle each candidate input and count how many
// state bits evolve over several edges (a real clock makes the CPU's registers move).
const W = './_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const fs = require('fs');
const N = 100000;
const data = JSON.parse(fs.readFileSync('./_z_pachinko\\_z_rev_inputs.json', 'utf8'));

// inputs that actually affect logic, excluding the three 16-bit buses 19..66
const buses = new Set();
for (let i = 19; i <= 66; i++) buses.add(i);
const cands = data.inputs.map(r => r.i).filter(i => !buses.has(i) && data.rows[i].diff > 2);
console.log('candidate clocks:', cands.length);

function evolveCount(bit, edges) {
  const s = new Uint8Array(N);
  wasmProcess(s);
  const seen = new Map(); // index -> Set of values
  const track = (st) => {
    for (let j = 0; j < 6000; j++) {
      if (!seen.has(j)) seen.set(j, new Set());
      seen.get(j).add(st[j]);
    }
  };
  track(s);
  for (let e = 0; e < edges; e++) {
    s[bit] = (s[bit] === 255) ? 0 : 255;
    wasmProcess(s);
    track(s);
  }
  let evolving = 0;
  for (const [, set] of seen) if (set.size > 1) evolving++;
  return evolving;
}

const results = cands.map(c => ({ bit: c, ev: evolveCount(c, 6) }))
  .sort((a, b) => b.ev - a.ev);
console.log('top 25 by evolving bits:');
for (const r of results.slice(0, 25)) console.log('  bit', r.bit, 'evolving', r.ev);
fs.writeFileSync('./_z_pachinko\\_z_clock_scan.json', JSON.stringify(results));
