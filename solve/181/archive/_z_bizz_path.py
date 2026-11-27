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

PLAY = 0x8049261
MAIN = 0x814cdd8          # jmp target of the jmp at 0x804911d (real main body)
TARGET = 0x808ba1f

# find callers: for each call to T, identify enclosing fn and the condition guard
callers = collections.defaultdict(list)   # callee -> [(fn, site, kind, cond, Nplay)]
for i, (a, t) in enumerate(insns):
    m = re.match(r'call\s+([0-9a-f]+)', t)
    if not m:
        continue
    callee = int(m.group(1), 16)
    if callee not in sset:
        continue
    f = fn_of(a)
    # pattern A: previous instrs: cmp <r>,K ; jne skip ; (call)   OR cmp ; je (call)
    kind = None; cond = None; Nplay = None
    # look back for cmp on eax or [ebp-0xc]
    for k in range(1, 8):
        a2, t2 = insns[i - k]
        if a2 < f:
            break
        mm = re.match(r'cmp\s+(?:eax|DWORD PTR \[ebp-0xc\]),(0x[0-9a-f]+)$', t2)
        if mm:
            K = int(mm.group(1), 16)
            # find the conditional jump right after
            a3, t3 = insns[i - k + 1]
            mj = re.match(r'(jne|je)\s+([0-9a-f]+)', t3)
            if mj:
                tgt = int(mj.group(2), 16)
                if mj.group(1) == 'jne':
                    cond = ('==', K) if (tgt > a) else None
                    if tgt > a:
                        cond = ('==', K)      # jne skips past the call => call iff r==K
                else:  # je
                    cond = ('!=', K) if (tgt > a) else ('==', K)
            break
    # find nearest preceding play target
    for k in range(1, 400):
        if i - k < 0:
            break
        a2, t2 = insns[i - k]
        if a2 < f:
            break
        if 'call' in t2 and str(PLAY) in t2:
            for b in range(1, 8):
                mm = re.match(r'push\s+(0x[0-9a-f]+)$', insns[i - k - b][1])
                if mm:
                    Nplay = int(mm.group(1), 16)
                    break
            break
    callers[callee].append((f, a, cond, Nplay))

# walk up from TARGET with DFS to MAIN
sys.setrecursionlimit(10000)
best = None

def dfs(cur, path, seen):
    global best
    if cur == MAIN:
        return path
    if cur in seen or len(path) > 60:
        return None
    seen = seen | {cur}
    for (f, site, cond, Nplay) in callers.get(cur, []):
        r = dfs(f, path + [(f, site, cond, Nplay, cur)], seen)
        if r:
            return r
    return None

path = dfs(TARGET, [], set())
if not path:
    print("NO PATH, callers known for target:", [(hex(f), hex(s), c, n) for f, s, c, n in callers.get(TARGET, [])])
    sys.exit(1)
print("PATH from main to target: %d hops" % len(path))
for f, site, cond, Nplay, callee in path:
    print("fn %s : at %s call %s   [play(%s) cond %s]" % (hex(f), hex(site), hex(callee), Nplay, cond))
json.dump([(f, site, cond, Nplay, callee) for f, site, cond, Nplay, callee in path], open('/tmp/path.json', 'w'))
