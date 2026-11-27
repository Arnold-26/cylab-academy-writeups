import re, sys, bisect, collections, json

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []   # (addr, text)
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    a = int(m.group(1), 16)
    insns.append((a, m.group(3).strip()))
insns.sort()
addrs = [a for a, _ in insns]
idx = {a: i for i, a in enumerate(addrs)}

PLAY = 0x8049261
starts = []
for a, t in insns:
    if t.startswith('push ebp') and 0x8049000 < a < 0x8150000:
        starts.append(a)
starts.sort()

def fn_of(a):
    i = bisect.bisect_right(starts, a) - 1
    return starts[i] if i >= 0 else None

def get(a):
    return insns[idx[a]][1] if a in idx else None

# For each function, find "call play" and parse the following if-chain
layers = {}       # fn -> dict(target=N, cases={r: ('fgets',size)|('call',target)|('jmp',addr)})
for f in starts:
    # find call play inside function
    i = idx[f]
    call_at = None
    while i < len(insns):
        a, t = insns[i]
        if a != f and a in set(starts) and a > f:
            break
        if t.startswith('call') and PLAY in t:
            call_at = a
            break
        i += 1
    if call_at is None:
        continue
    # preceding push imm = target
    prev = get(call_at - 5)
    N = None
    j = idx[call_at] - 1
    for k in range(6):
        a2, t2 = insns[j - k]
        m = re.match(r'push (0x[0-9a-f]+)', t2)
        if m:
            N = int(m.group(1), 16)
            break
    # the return value of play -> [ebp-0xc]
    # now scan forward for cmp DWORD PTR [ebp-0xc],K
    cases = {}
    j = idx[call_at]
    while j < len(insns):
        a2, t2 = insns[j]
        if a2 in set(starts) and a2 > call_at:
            break
        if t2.startswith('call') and 'fgets' in t2:
            # find size push above and the case r
            size = None
            for k in range(1, 6):
                aa, tt = insns[j - k]
                mm = re.match(r'push (0x[0-9a-f]+)', tt)
                if mm and int(mm.group(1), 16) > 0x2:
                    size = int(mm.group(1), 16)
                    break
            cases.setdefault(cur_r, []).append(('fgets', size))
        elif t2.startswith('call ') and 'plt' not in t2 and '804' not in t2.split()[1][:4]:
            pass
        if t2.startswith('call'):
            mm = re.match(r'call\s+([0-9a-f]+)', t2)
            if mm and 'plt' not in t2:
                cases.setdefault(cur_r, []).append(('call', int(mm.group(1), 16)))
        m = re.match(r'cmp DWORD PTR \[ebp-0xc\],(0x[0-9a-f]+)', t2)
        if m:
            cur_r = int(m.group(1), 16)
        m = re.match(r'je\s+([0-9a-f]+)', t2)
        if m and cur_r is not None:
            cases.setdefault(cur_r, []).append(('jmp', int(m.group(1), 16)))
        j += 1
    layers[f] = {'N': N, 'cases': {k: v for k, v in cases.items()}}

print("layers found:", len(layers))
json.dump({hex(k): {'N': v['N'], 'cases': {str(r): c for r, c in v['cases'].items()}} for k, v in layers.items()},
          open('/tmp/layers.json', 'w'), indent=0)
# show the interesting ones
for f in (0x804911d, 0x814cdd8, 0x810aab4, 0x808ba1f, 0x8131f64, 0x8144ba9, 0x81417da):
    v = layers.get(f)
    if v:
        print(hex(f), 'N=', v['N'], 'cases:', {r: c for r, c in sorted(v['cases'].items()) if any(x[0] == 'call' for x in c)})
    else:
        print(hex(f), 'not a layer fn')
