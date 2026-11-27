// 478 Pachinko — run the /check program long enough to finish, log where PC goes
// and any non-zero value on the candidate out_val bus (35..50).
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
const nGates = Number(process.argv[2] || 1);
const outMem = new Uint16Array(mem.buffer, 0x1000);
outMem[0] = 4; for (let i = 0; i < 4; i++) outMem[1 + i] = 0xffff;
const inMem = new Uint16Array(mem.buffer, 0x2000);
for (let i = 0; i < 4; i++) inMem[5 + i] = 0x0000;
// one circuit gate at 0x3000
const circ = new Uint16Array(mem.buffer, 0x3000);
for (let g = 0; g < nGates; g++) { circ[3 * g] = 0x0fff; circ[3 * g + 1] = 0x0fff; circ[3 * g + 2] = 0xf000; }

const s = new Uint8Array(N);
wasmProcess(s);
s[RESET] = 255; wasmProcess(s);
s[RESET] = 0; wasmProcess(s);
const CYCLES = Number(process.argv[3] || 3000);
const pcSeen = new Map();
let lastPc = -1, run = 0;
for (let c = 0; c < CYCLES; c++) {
  s[CLOCK] ^= 255;
  wasmProcess(s);
  if (s[CLOCK] !== 0) continue;
  const addr = getVal(s, ADDR);
  setVal(s, INP, mem[addr] | (mem[addr + 1] << 8));
  pcSeen.set(addr, (pcSeen.get(addr) || 0) + 1);
  const ov = getVal(s, OUT);
  if (ov !== 0) console.log(`c=${c} pc=${addr.toString(16)} out35_50=${ov.toString(16)}`);
  if (addr === lastPc) run++; else { lastPc = addr; run = 1; }
}
const pcs = [...pcSeen.keys()].sort((a, b) => a - b);
console.log('distinct PCs:', pcs.map(x => x.toString(16)).join(','));
console.log('counts:', pcs.map(x => x.toString(16) + ':' + pcSeen.get(x)).join(' '));
