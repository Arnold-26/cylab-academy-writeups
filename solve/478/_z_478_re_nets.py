#!/usr/bin/env python3
"""Classify every net of the synthesized CPU by how the wasm touches it.

Each net is a byte offset in the state buffer, and codegen always spells it as a
literal: `i32.load8_u offset=N` to read, `i32.store8 offset=N` to write.
  inputs  = read but never written   (primary inputs of cpu.json)
  outputs = written but never read   (primary outputs of cpu.json)
"""
import re, json, collections

WAT = '/tmp/cpu.wat'
read = collections.Counter()
written = collections.Counter()
pat = re.compile(r'^i32\.(load8_u|load8_s|store8)(?: offset=(\d+))?')
for ln in open(WAT, 'r', errors='replace'):
    m = pat.match(ln.strip())
    if not m:
        continue
    off = int(m.group(2)) if m.group(2) is not None else 0
    if m.group(1).startswith('load'):
        read[off] += 1
    else:
        written[off] += 1

R, W = set(read), set(written)
inputs = sorted(R - W)
outputs = sorted(W - R)
print('nets read   :', len(R))
print('nets written:', len(W))
print('PRIMARY INPUTS (%d):' % len(inputs))
print(inputs)
print('PRIMARY OUTPUTS (%d):' % len(outputs))
print(outputs)
# contiguous-run summary
def runs(xs):
    out = []
    for x in xs:
        if out and x == out[-1][1] + 1: out[-1][1] = x
        else: out.append([x, x])
    return out
print('input runs :', runs(inputs))
print('output runs:', runs(outputs))
json.dump({'inputs': inputs, 'outputs': outputs,
           'read': {k: v for k, v in read.items()},
           'written': {k: v for k, v in written.items()}},
          open('/mnt/d/ctf-index/_z_pachinko/_z_nets.json', 'w'))
