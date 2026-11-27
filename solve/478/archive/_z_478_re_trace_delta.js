// 478 Pachinko — compact trace: per cycle, PC, out_val(35..50), and which low bits changed.
const W = './_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const fs = require('fs');
const N = 100000;
const CLOCK = 2, RESET = 68;
const rng = (a) => Array.from({ length: 16 }, (_, k) => a + k);
const ADDR = rng(51), INP = rng(19), OUT = rng(35);
function getVal(s, bits) { let r = 0; for (let i = 0; i < bits.length; i++) r |= ((s[bits[i]] >> 7) & 1) << i; return r; }
function setVal(s, bits, v) { for (let i = 0; i < bits.length; i++) s[bits[i]] = ((v >> i) & 1) ? 255 : 0; }

const program = fs.readFileSync('./_z_pachinko\\server\\programs\\nand_checker.bin');
const mem = new Uint8Array(65536);
mem.set(program);
const outView = new Uint16Array(mem.buffer, 0x1000);
outView[0] = 4; for (let i = 0; i < 4; i++) outView[1 + i] = 0xffff;
const inView = new Uint16Array(mem.buffer, 0x2000);
for (let i = 0; i < 4; i++) inView[5 + i] = 0x0000;

const s = new Uint8Array(N);
wasmProcess(s);
s[RESET] = 255; wasmProcess(s);
s[RESET] = 0; wasmProcess(s);
const CYCLES = Number(process.argv[2] || 300);
let prev = null;
for (let c = 0; c < CYCLES; c++) {
  s[CLOCK] ^= 255;
  wasmProcess(s);
  if (s[CLOCK] !== 0) continue;
  const addr = getVal(s, ADDR);
  setVal(s, INP, mem[addr] | (mem[addr + 1] << 8));
  const cur = [];
  for (let i = 0; i <= 176; i++) if (s[i] === 255) cur.push(i);
  const curSet = new Set(cur);
  const delta = prev ? cur.filter(x => !prev.has(x)).map(x => '+' + x)
    .concat([...prev].filter(x => !curSet.has(x)).map(x => '-' + x)) : cur.map(x => '+' + x);
  prev = curSet;
  if (delta.length) console.log(`c=${String(c).padStart(3)} pc=${addr.toString(16).padStart(4, '0')} out=${getVal(s, OUT).toString(16).padStart(4, '0')} d=[${delta.join(' ')}]`);
}
