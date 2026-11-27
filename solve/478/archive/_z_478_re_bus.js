// 478 Pachinko — with a candidate clock, sample the three 16-bit buses each edge.
// A PC shows up as a bus that advances by a constant step every edge.
const W = './_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const N = 100000;

function val(s, bits, order) {
  let r = 0;
  const list = order === 'msb' ? [...bits].reverse() : bits;
  for (let i = 0; i < list.length; i++) r |= ((s[list[i]] >> 7) & 1) << i;
  return r;
}
const busA = Array.from({ length: 16 }, (_, k) => 19 + k);
const busB = Array.from({ length: 16 }, (_, k) => 35 + k);
const busC = Array.from({ length: 16 }, (_, k) => 51 + k);

function trace(clock, resetBit, edges) {
  const s = new Uint8Array(N);
  wasmProcess(s);
  if (resetBit !== null) {
    s[resetBit] = 255; wasmProcess(s);
    s[resetBit] = 0; wasmProcess(s);
  }
  const out = [];
  for (let e = 0; e < edges; e++) {
    s[clock] ^= 255;
    wasmProcess(s);
    out.push({
      e, clk: s[clock],
      A: val(s, busA, 'lsb'), B: val(s, busB, 'lsb'), C: val(s, busC, 'lsb'),
    });
  }
  return out;
}

for (const [clock, reset, label] of [[68, null, 'clk=68 noreset'], [68, 2, 'clk=68 rst=2'], [2, 68, 'clk=2 rst=68'], [70, 68, 'clk=70 rst=68']]) {
  console.log('=== ' + label);
  const t = trace(clock, reset, 24);
  for (const r of t) console.log(`e=${String(r.e).padStart(2)} clk=${String(r.clk).padStart(3)} A=${r.A.toString(16).padStart(4, '0')} B=${r.B.toString(16).padStart(4, '0')} C=${r.C.toString(16).padStart(4, '0')}`);
}
