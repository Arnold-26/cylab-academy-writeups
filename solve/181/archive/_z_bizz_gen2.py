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
starts = sorted(a for a, t in insns if t.startswith('push ebp') and 0x8049000 < a < 0x8150000)
PLT = 0x8049100
PLAY = 0x8049261
MAIN = 0x814cdd8
THUNKS = {0x8049140, 0x814d276}

def tgt(t):
    m = re.match(r'call\s+([0-9a-f]+)', t)
    return int(m.group(1), 16) if m else None

def fn_end(f):
    begin = idx.get(f)
    for i in range(begin, min(begin + 4000, len(insns) - 1)):
        if insns[i][1] == 'leave' and insns[i + 1][1] == 'ret':
            return insns[i + 1][0]
    return 0x8150000

def events(lo, hi):
    out = []
    for i, (a, t) in enumerate(insns):
        if not (lo <= a <= hi):
            continue
        if re.match(r'push\s+(0x[0-9a-f]+|\d+)$', t):
            for k in (1, 2):
                if i + k < len(insns) and insns[i + k][1].startswith('call') and tgt(insns[i + k][1]) == PLAY:
                    out.append((a, 'play', int(t.split()[1], 0)))
                    break
        elif t.startswith('call'):
            c = tgt(t)
            if c == PLAY:
                continue
            if c and c >= PLT and c not in THUNKS:
                out.append((a, 'call', c))
        elif re.match(r'(je|jne)\s+([0-9a-f]+)', t):
            m = re.match(r'(je|jne)\s+([0-9a-f]+)', t)
            out.append((a, m.group(1), int(m.group(2), 16)))
    return out

def first_play(f):
    for a, k, v in events(f, fn_end(f)):
        if k == 'play':
            return v
    return None

def ladder(f, stop_callee):
    res, cur = [], None
    for a, k, v in events(f, fn_end(f)):
        if k == 'play':
            cur = v
        elif k == 'call':
            if cur is None:
                print("ATTENTION call sans play dans %x a %x" % (f, a), file=sys.stderr)
                continue
            res.append((cur, v))
            if v == stop_callee:
                return res
            cur = None
    return res

def fizz(i):
    if i % 15 == 0:
        return 'fizzbuzz'
    if i % 3 == 0:
        return 'fizz'
    if i % 5 == 0:
        return 'buzz'
    return str(i)

stream, rounds, tags = [], [], []

def round_(N, answers, tag):
    rounds.append(N)
    tags.append("%d %s" % (N, tag))
    for a in answers:
        stream.append(a)

# main prefix
for c in [v for a, k, v in events(MAIN, 0x814d0f0) if k == 'call']:
    fp = first_play(c)
    if fp is None:
        print("!! pas de premier play %x" % c, file=sys.stderr)
        continue
    round_(fp, [fizz(i) for i in range(1, fp)], "main-fastexit %x" % c)

for f, stop in ((0x813d5dc, 0x8144ba9), (0x8144ba9, 0x8131f64), (0x8131f64, 0x810aab4)):
    lad = ladder(f, stop)
    print("%x : %d etages -> %x" % (f, len(lad), lad[-1][1]), file=sys.stderr)
    for N, callee in lad:
        round_(N, ['x'] if N > 1 else [], "hop %x play(%d) WRONG" % (f, N))
        if callee != stop:
            fp = first_play(callee)
            if fp is None:
                print("!! pas de play pour fastexit %x" % callee, file=sys.stderr)
                continue
            round_(fp, [fizz(i) for i in range(1, fp)], "fastexit %x" % callee)

round_(46, [fizz(1), fizz(2), fizz(3), fizz(4), 'x'], "hop4 r=5")
round_(20, ['x'], "hop5 r=1")

blob = b"".join(a.encode() + b"\n" for a in stream)
open('/tmp/bizz_stream.bin', 'wb').write(blob)
open('/tmp/bizz_rounds.txt', 'w').write("\n".join(str(n) for n in rounds))
open('/tmp/bizz_tags.txt', 'w').write("\n".join(tags))
print("answers:", len(stream), "rounds:", len(rounds), "bytes:", len(blob))
