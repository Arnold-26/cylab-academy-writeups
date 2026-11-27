import re, sys

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    insns.append((int(m.group(1), 16), ' '.join(m.group(3).split())))
insns.sort()
idx = {a: i for i, (a, t) in enumerate(insns)}
PLAY = '8049261'

def summarize(lo, hi, title):
    print("=" * 20, title, hex(lo), "-", hex(hi))
    last_play = None
    for i, (a, t) in enumerate(insns):
        if not (lo <= a <= hi):
            continue
        if re.match(r'push\s+(0x[0-9a-f]+|\d+)$', t):
            # look ahead 2 for call play
            for k in range(1, 3):
                if i + k < len(insns) and 'call' in insns[i + k][1] and PLAY in insns[i + k][1]:
                    print("%s  PLAY(%s)" % (hex(a), t.split()[1]))
                    last_play = a
                    break
        elif t.startswith('call') and PLAY not in t:
            m = re.match(r'call\s+([0-9a-f]+)', t)
            print("%s  call %s" % (hex(a), m.group(1)))
        elif t.startswith('fgets') or 'fgets@plt' in t:
            print("%s  FGETS" % hex(a, ))
        elif re.match(r'(je|jne)\s+([0-9a-f]+)$', t):
            print("%s  %s %s" % (hex(a), t.split()[0], t.split()[1]))
        elif t.startswith('call') and PLAY in t:
            pass

for lo, hi, title in [
    (0x814cdd8, 0x814d0f5, "main up to hop1 call"),
    (0x813d5dc, 0x813d6e0, "hop1 fn 813d5dc"),
    (0x8144ba9, 0x8144bf0, "hop2 fn 8144ba9"),
    (0x8131f64, 0x81321e0, "hop3 fn 8131f64"),
]:
    summarize(lo, hi, title)
