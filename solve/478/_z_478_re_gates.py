#!/usr/bin/env python3
"""Extract the NAND gate list from the WAT dump of verilog_ctf_wasm_bg.wasm.

Rust source:  *p.add(y) = !(*p.add(a) & *p.add(b));   (p = base pointer local)
wasm emits, for each gate:
   local.get P ; local.get P ; i32.load8_u offset=A   [; local.get P ; i32.load8_u offset=B ; i32.and]
   i32.const -1 ; i32.xor ; i32.store8 offset=Y
When a == b the AND is folded away, so a lone load means an inverter (a == b).
"""
import re, json, sys

WAT = '/tmp/cpu.wat'
ops = []   # (op, offset)
pat = re.compile(r'^(i32\.load8_u|i32\.load8_s|i32\.store8|i32\.and|i32\.xor|i32\.const)(?: offset=(\d+))?(?:\s+(-?\d+))?')
for ln in open(WAT, 'r', errors='replace'):
    s = ln.strip()
    m = pat.match(s)
    if not m:
        continue
    op, off, val = m.group(1), m.group(2), m.group(3)
    off = int(off) if off is not None else 0
    ops.append((op, off, val))

gates = []
i = 0
n = len(ops)
while i < n:
    if ops[i][0] == 'i32.store8':
        y = ops[i][1]
        # walk back
        a = b = None
        saw_and = False
        j = i - 1
        steps = 0
        while j >= 0 and steps < 12:
            o = ops[j][0]
            if o == 'i32.store8' or o == 'i32.store':
                break
            if o in ('i32.load8_u', 'i32.load8_s'):
                if a is None:
                    a = ops[j][1]
                elif b is None:
                    b = ops[j][1]
            elif o == 'i32.and':
                saw_and = True
            j -= 1
            steps += 1
        if a is not None:
            if not saw_and or b is None:
                b = a
            gates.append([a, b, y])
    i += 1

print('total gates:', len(gates))
dst = set(g[2] for g in gates)
print('distinct dst:', len(dst), 'max dst', max(dst), 'min dst', min(dst))
srcs = set()
for g in gates:
    srcs.add(g[0]); srcs.add(g[1])
print('distinct src:', len(srcs), 'max src', max(srcs))
fan = {}
for g in gates:
    for s in (g[0], g[1]):
        fan[s] = fan.get(s, 0) + 1
zero = sorted(srcs - dst)
print('read-but-never-written nets (primary inputs):', len(zero))
print(zero)
outonly = sorted(dst - srcs)
print('written-but-never-read nets (primary outputs):', len(outonly))
print(outonly)
json.dump(gates, open('/mnt/d/ctf-index/_z_pachinko/_z_gates.json', 'w'))
