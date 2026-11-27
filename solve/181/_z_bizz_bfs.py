import re, bisect, collections, json, sys

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    insns.append((int(m.group(1), 16), ' '.join(m.group(3).split())))
insns.sort()
starts = sorted(a for a, t in insns if t.startswith('push ebp') and 0x8049000 < a < 0x8150000)
starts = sorted(set(starts) | {0x814cdd8, 0x804911d})
sset = set(starts)

def fn_of(a):
    i = bisect.bisect_right(starts, a) - 1
    return starts[i] if i >= 0 else None

edges = collections.defaultdict(list)    # fn -> [(callee, site)]
for a, t in insns:
    m = re.match(r'call\s+([0-9a-f]+)', t)
    if not m:
        continue
    c = int(m.group(1), 16)
    if c in sset:
        f = fn_of(a)
        edges[f].append((c, a))

MAIN = 0x814cdd8
TARGET = 0x808ba1f
# BFS
prev = {MAIN: None}
q = collections.deque([MAIN])
found = False
while q and not found:
    n = q.popleft()
    for c, site in edges[n]:
        if c not in prev:
            prev[c] = (n, site)
            if c == TARGET:
                found = True
                break
            q.append(c)
if TARGET not in prev:
    print("no path")
    sys.exit(1)
path = []
n = TARGET
while prev[n]:
    p, site = prev[n]
    path.append((p, site, n))
    n = p
path.reverse()
print("path hops:", len(path))
for p, site, n in path:
    print("  %s --call@%s--> %s" % (hex(p), hex(site), hex(n)))
json.dump([(p, site, n) for p, site, n in path], open('/tmp/path2.json', 'w'))
