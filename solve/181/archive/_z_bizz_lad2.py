import re, sys

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    insns.append((int(m.group(1), 16), ' '.join(m.group(3).split())))
insns.sort()
PLAY = '8049261'

def summarize(lo, hi, title):
    print("=" * 20, title, hex(lo), "-", hex(hi))
    for i, (a, t) in enumerate(insns):
        if not (lo <= a <= hi):
            continue
        if re.match(r'push\s+(0x[0-9a-f]+|\d+)$', t):
            for k in range(1, 3):
                if i + k < len(insns) and insns[i + k][1].startswith('call') and PLAY in insns[i + k][1]:
                    print("  %s PLAY(%s)" % (hex(a), hex(int(t.split()[1], 0))))
                    break
        elif t.startswith('call') and 'plt' not in t:
            m = re.match(r'call\s+([0-9a-f]+)', t)
            tgt = m.group(1)
            # skip the ebx thunks
            if tgt in ('8049140', '814d276', '80491d0', '8049180'):
                continue
            print("  %s call %s" % (hex(a), tgt))
        elif t.startswith('call'):
            m = re.match(r'call\s+([0-9a-f]+)', t)
            if 'fgets' in t:
                print("  %s FGETS" % hex(a))
        elif re.match(r'(je|jne)\s', t):
            print("  %s %s" % (hex(a), t))

for lo, hi, title in [
    (0x813d5dc, 0x813d700, "hop1 813d5dc"),
    (0x8144ba9, 0x8144bf5, "hop2 8144ba9"),
    (0x8131f64, 0x81321e5, "hop3 8131f64"),
    (0x810aab4, 0x810ab50, "hop4 810aab4 (switch)"),
    (0x808ba1f, 0x808ba70, "hop5 808ba1f (vuln)"),
]:
    summarize(lo, hi, title)
