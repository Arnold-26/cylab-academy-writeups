// 478 Pachinko — cycle-by-cycle trace on the real /check memory image.
// Ports known: clock=2, reset=68, inp_val=19..34, out_val=35..50, addr=51..66.
// Goal: find write_enable / halted / flag, and see the store cycle.
const W = 'D:\\ctf-index\\_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const fs = require('fs');
const N = 100000;
const CLOCK = 2, RESET = 68;
const rng = (a) => Array.from({ length: 16 }, (_, k) => a + k);
const ADDR = rng(51), INP = rng(19), OUT = rng(35);
function getVal(s, bits) { let r = 0; for (let i = 0; i < bits.length; i++) r |= ((s[bits[i]] >> 7) & 1) << i; return r; }
function setVal(s, bits, v) { for (let i = 0; i < bits.length; i++) s[bits[i]] = ((v >> i) & 1) ? 255 : 0; }

const program = fs.readFileSync('D:\\ctf-index\\_z_pachinko\\server\\programs\\nand_checker.bin');
const mem = new Uint8Array(65536);
mem.set(program);
// output state at 0x1000, input state at 0x2000 exactly as serializeCircuit does
const outView = new Uint16Array(mem.buffer, 0x1000);
outView[0] = 4; for (let i = 0; i < 4; i++) outView[1 + i] = 0xffff;
const inView = new Uint16Array(mem.buffer, 0x2000);
for (let i = 0; i < 4; i++) inView[5 + i] = 0x0000;

const s = new Uint8Array(N);
wasmProcess(s);
s[RESET] = 255; wasmProcess(s);
s[RESET] = 0; wasmProcess(s);
const CYCLES = Number(process.argv[2] || 80);
for (let c = 0; c < CYCLES; c++) {
  s[CLOCK] ^= 255;
  wasmProcess(s);
  if (s[CLOCK] !== 0) continue;
  const addr = getVal(s, ADDR);
  setVal(s, INP, mem[addr] | (mem[addr + 1] << 8));
  const bits = [];
  for (let i = 0; i <= 260; i++) if (s[i] === 255) bits.push(i);
  console.log(`c=${String(c).padStart(3)} pc=${addr.toString(16).padStart(4, '0')} out=${getVal(s, OUT).toString(16).padStart(4, '0')} ones=[${bits.join(',')}]`);
}
