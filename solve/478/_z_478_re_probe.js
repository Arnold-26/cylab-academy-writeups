// 478 Pachinko — reverse the Verilog CPU netlist from the compiled wasm.
// Step 1: partition state[] into gate outputs vs netlist inputs.
const path = require('path');
const W = './_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);

const N = 100000;
function run(fill, pre) {
  const s = new Uint8Array(N);
  if (fill !== null) s.fill(fill);
  if (pre) pre(s);
  wasmProcess(s);
  return s;
}

const a = run(0);    // every gate -> 255
const b = run(255);  // every gate -> 0

const driven = [];
const inputs = [];
const weird = [];
for (let i = 0; i < N; i++) {
  if (a[i] === 255 && b[i] === 0) driven.push(i);
  else if (a[i] === 0 && b[i] === 255) inputs.push(i);
  else if (a[i] === 0 && b[i] === 0) weird.push([i, a[i], b[i]]);
  else weird.push([i, a[i], b[i]]);
}
console.log('driven', driven.length, 'stayed-fill', inputs.length, 'weird', weird.length);
console.log('driven first/last', driven[0], driven[driven.length - 1]);
// netlist-input candidates = indices that keep the fill value in BOTH runs
const in0 = [];
for (let i = 0; i < N; i++) if (a[i] === 0 && b[i] === 255) in0.push(i);
// restrict to below max used index
const maxUsed = Math.max(driven[driven.length - 1], ...in0.filter(i => i < 5000));
const cand = in0.filter(i => i < driven[driven.length - 1]);
console.log('inputs below maxDriven', cand.length);
console.log('first 80 inputs:', JSON.stringify(cand.slice(0, 80)));
console.log('weird sample:', JSON.stringify(weird.slice(0, 20)));
