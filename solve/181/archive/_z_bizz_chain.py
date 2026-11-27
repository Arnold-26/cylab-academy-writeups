import re, bisect, collections, json, sys

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    insns.append((int(m.group(1), 16), ' '.join(m.group(3).split())))
insns.sort()
idx = {a: i for i, (a, _) in enumerate(insns)}
starts = sorted(a for a, t in insns if t.startswith('push ebp') and 0x8049000 < a < 0x8150000)
sset = set(starts)

def fn_of(a):
    i = bisect.bisect_right(starts, a) - 1
    return starts[i] if i >= 0 else None

edges = collections.defaultdict(list)   # fn -> [(r, callee, callsite)]
for i, (a, t) in enumerate(insns):
    m = re.match(r'call\s+([0-9a-f]+)', t)
    if not m:
        continue
    tgt = int(m.group(1), 16)
    if tgt not in sset:
        continue
    f = fn_of(a)
    # find most recent cmp [ebp-0xc],K before
    r = None
    for k in range(1, 200):
        if i - k < 0:
            break
        a2, t2 = insns[i - k]
        if a2 < f:
            break
        mm = re.match(r'cmp DWORD PTR \[ebp-0xc\],(0x[0-9a-f]+)', t2)
        if mm:
            r = int(mm.group(1), 16)
            break
    edges[f].append((r, tgt, a))

# play target per function
playtarget = {}
for f in starts:
    i0 = idx[f]
    for k in range(0, 60):
        if i0 + k >= len(insns):
            break
        a2, t2 = insns[i0 + k]
        if a2 in sset and a2 != f:
            break
        if 'call' in t2 and '8049261' in t2:
            for b in range(1, 8):
                mm = re.match(r'push (0x[0-9a-f]+)', insns[i0 + k - b][1])
                if mm:
                    playtarget[f] = int(mm.group(1), 16)
                    break
            break

TGT = 0x808ba1f
# backwards BFS
rev = collections.defaultdict(list)
for f, lst in edges.items():
    for r, tgt, site in lst:
        rev[tgt].append((f, r, site))

path = []
node = TGT
seen = set()
while True:
    if node in seen:
        print("loop")
        break
    seen.add(node)
    if not rev[node]:
        break
    f, r, site = rev[node][0]
    path.append((f, playtarget.get(f), r, node, site))
    node = f
print("chain length:", len(path))
for f, N, r, callee, site in reversed(path):
    print("fn %s  asks play(%s)  r=%s -> call %s" % (hex(f), N, r, hex(callee)))
print()
print("entry node:", hex(node), "playtarget:", playtarget.get(node))
json.dump([(f, playtarget.get(f), r, callee) for f, N, r, callee, site in reversed(path)],
          open('/tmp/chain.json', 'w'))
