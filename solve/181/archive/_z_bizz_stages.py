import re, json, sys

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    insns.append((int(m.group(1), 16), ' '.join(m.group(3).split())))
insns.sort()
idx = {a: i for i, (a, t) in enumerate(insns)}
starts = sorted(a for a, t in insns if t.startswith('push ebp') and 0x8049000 < a < 0x8150000)
PLT_LIMIT = 0x8049100
PLAY = 0x8049261

def is_call(t):
    return t.startswith('call ')

def call_tgt(t):
    m = re.match(r'call\s+([0-9a-f]+)', t)
    return int(m.group(1), 16) if m else None

def stages(lo, hi):
    """retourne [(addr, kind, val)] : ('play',N) ('call',tgt) ('je',tgt)"""
    out = []
    for i, (a, t) in enumerate(insns):
        if not (lo <= a <= hi):
            continue
        if re.match(r'push\s+(0x[0-9a-f]+|\d+)$', t):
            for k in (1, 2):
                if i + k < len(insns) and is_call(insns[i + k][1]) and call_tgt(insns[i + k][1]) == PLAY:
                    out.append((a, 'play', int(t.split()[1], 0)))
                    break
        elif is_call(t):
            c = call_tgt(t)
            if c and c >= PLT_LIMIT:
                out.append((a, 'call', c))
            elif c and c < PLT_LIMIT and 'fgets' in t:
                out.append((a, 'fgets', c))
        elif re.match(r'(je|jne)\s+([0-9a-f]+)', t):
            m = re.match(r'(je|jne)\s+([0-9a-f]+)', t)
            out.append((a, m.group(1), int(m.group(2), 16)))
    return out

if __name__ == '__main__':
    for lo, hi, title in [
        (0x8131f64, 0x81321e5, "hop3 8131f64"),
        (0x810aab4, 0x810ab50, "hop4 810aab4"),
        (0x808ba1f, 0x808ba70, "hop5 808ba1f"),
    ]:
        print("=" * 15, title)
        for s in stages(lo, hi):
            print("  ", hex(s[0]), s[1], hex(s[2]) if isinstance(s[2], int) else s[2])
