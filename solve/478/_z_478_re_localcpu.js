// 478 Pachinko — local replica of cpu.js runCPU with a configurable port map.
// Discovered so far: clock = 2, reset = 68, PC/addr = bits 51..66 (advances by 2/cycle).
// Unknowns: which bus is inp_val vs out_val (19..34 / 35..50), and the
// single-bit control nets write_enable / halted / flag.
const W = 'D:\\ctf-index\\_z_pachinko\\server\\wasm\\pkg\\verilog_ctf_wasm.js';
const { process: wasmProcess } = require(W);
const fs = require('fs');
const N = 100000;

const range = (a) => Array.from({ length: 16 }, (_, k) => a + k);
function getVal(s, bits) { let r = 0; for (let i = 0; i < bits.length; i++) r |= ((s[bits[i]] >> 7) & 1) << i; return r; }
function setVal(s, bits, v) { for (let i = 0; i < bits.length; i++) s[bits[i]] = ((v >> i) & 1) ? 255 : 0; }

const CLOCK = 2, RESET = 68;

function runCPU(memory, cfg, maxCycles) {
  const s = new Uint8Array(N);
  wasmProcess(s);
  s[RESET] = 255; wasmProcess(s);
  s[RESET] = 0; wasmProcess(s);
  const addrBits = cfg.addr, inpBits = cfg.inp, outBits = cfg.out;
  const log = [];
  let flag = false, halted = false;
  for (let cycle = 0; cycle < maxCycles; cycle++) {
    s[CLOCK] ^= 255;
    wasmProcess(s);
    if (s[CLOCK] === 0) {
      const addr = getVal(s, addrBits);
      const ow = cfg.we ? getVal(s, [cfg.we]) : 0;
      const outv = getVal(s, outBits);
      if (ow) { memory[addr] = outv & 0xff; memory[addr + 1] = (outv >> 8) & 0xff; }
      setVal(s, inpBits, memory[addr] | (memory[addr + 1] << 8));
      log.push({ cycle, addr, ow, outv });
      if (cfg.halted && getVal(s, [cfg.halted])) { halted = true; log.push({ halted: true }); break; }
      if (cfg.flag && getVal(s, [cfg.flag])) flag = true;
    }
  }
  return { s, log, flag, halted };
}

// which single bits changed to 255 after running flag.bin, vs running empty memory?
function hotBits(s, base) {
  const out = [];
  for (let i = 0; i < 6000; i++) if (s[i] === 255 && base[i] !== 255) out.push(i);
  return out;
}

const flagBin = fs.readFileSync('D:\\ctf-index\\_z_pachinko\\server\\programs\\flag.bin');
const cfg = { addr: range(51), inp: range(19), out: range(35), we: null, halted: null, flag: null };
const memEmpty = new Uint8Array(65536);
const r0 = runCPU(memEmpty, cfg, 60);
const memFlag = new Uint8Array(65536); memFlag.set(flagBin);
const r1 = runCPU(memFlag, cfg, 60);

console.log('empty  addr seq:', r0.log.filter(x => x.addr !== undefined).map(x => x.addr.toString(16)).join(' '));
console.log('flagbin addr seq:', r1.log.filter(x => x.addr !== undefined).map(x => x.addr.toString(16)).join(' '));
console.log('empty  outv non-zero:', r0.log.filter(x => x.outv).slice(0, 8));
console.log('flagbin outv non-zero:', r1.log.filter(x => x.outv).slice(0, 8));
const hb = hotBits(r1.s, r0.s);
console.log('bits that are 255 with flag.bin but not with empty mem:', JSON.stringify(hb));
