// 478 Pachinko — isolate the CPU's `flag` net.
// flag.bin = 4x LDI, then 0x000e, then 0x000f. Substituting 0x000e with 0x0000
// (same instruction length) keeps control flow identical and removes only the
// flag-raising side effect, so the diff of the final states is the flag + fanout.
const W = './_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const fs = require('fs');
const N = 100000;
const CLOCK = 2, RESET = 68;
const rng = (a) => Array.from({ length: 16 }, (_, k) => a + k);
const ADDR = rng(51), INP = rng(19);
function getVal(s, bits) { let r = 0; for (let i = 0; i < bits.length; i++) r |= ((s[bits[i]] >> 7) & 1) << i; return r; }
function setVal(s, bits, v) { for (let i = 0; i < bits.length; i++) s[bits[i]] = ((v >> i) & 1) ? 255 : 0; }

function run(mem, cycles) {
  const s = new Uint8Array(N);
  wasmProcess(s);
  s[RESET] = 255; wasmProcess(s);
  s[RESET] = 0; wasmProcess(s);
  const pcs = [];
  for (let c = 0; c < cycles; c++) {
    s[CLOCK] ^= 255;
    wasmProcess(s);
    if (s[CLOCK] !== 0) continue;
    const addr = getVal(s, ADDR);
    pcs.push(addr);
    setVal(s, INP, mem[addr] | (mem[addr + 1] << 8));
  }
  return { s, pcs };
}

const flagBin = fs.readFileSync('./_z_pachinko\\server\\programs\\flag.bin');
const A = new Uint8Array(65536); A.set(flagBin);
const B = Uint8Array.from(A); B[0x10] = 0; B[0x11] = 0;   // neutralise the 0x000e instruction

const ra = run(A, 60), rb = run(B, 60);
console.log('pcA:', ra.pcs.map(x => x.toString(16)).join(','));
console.log('pcB:', rb.pcs.map(x => x.toString(16)).join(','));
const diff = [];
for (let i = 0; i < 6000; i++) if (ra.s[i] !== rb.s[i]) diff.push([i, rb.s[i], ra.s[i]]);
console.log('bits differing (index, B_val, A_val):');
console.log(JSON.stringify(diff));
