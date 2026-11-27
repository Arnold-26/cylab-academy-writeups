# 181 - Bizz Fuzz  (Binary Exploitation, picoCTF 2021)
# Flag: academy{y0u_found_m3}
# Write-up: ../../../writeups/binary-exploitation/181-bizz-fuzz.md
# Script exact utilise pour produire le flag.
#
import re, sys, json

lines = open('/tmp/bizz.asm').read().split('\n')
insns = []
for l in lines:
    m = re.match(r'^ *([0-9a-f]+):\t([0-9a-f ]+)\t([a-z].*)$', l)
    if not m:
        continue
    insns.append((int(m.group(1), 16), ' '.join(m.group(3).split())))
insns.sort()
idx = {a: i for i, (a, t) in enumerate(insns)}
addrs = [a for a, _ in insns]
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
    if begin is None:
        return f
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
            elif c and c < PLT:
                out.append((a, 'plt', c))
        elif re.match(r'(je|jne)\s+([0-9a-f]+)', t):
            m = re.match(r'(je|jne)\s+([0-9a-f]+)', t)
            out.append((a, m.group(1), int(m.group(2), 16)))
    return out

def first_play(f):
    ev = events(f, fn_end(f))
    for a, k, v in ev:
        if k == 'play':
            return v
    return None

def ladder(f, stop_callee):
    """[(N, callee)] jusqu'a l'etage dont le callee == stop_callee (inclus)."""
    res = []
    cur = None
    for a, k, v in events(f, fn_end(f)):
        if k == 'play':
            cur = v
        elif k == 'call':
            if cur is None:
                print("ATTENTION: call sans play dans %x" % f, file=sys.stderr)
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

def correct(N):
    return [fizz(i) for i in range(1, N)]

def wrong(N):
    assert N > 1, "impossible de rater play(%d)" % N
    return ['x']

HOP = [0x813d5dc, 0x8144ba9, 0x8131f64, 0x810aab4, 0x808ba1f]
stream = []
log = []

def emit(ans, tag):
    stream.append(ans)
    log.append((ans, tag))

# --- main : appels avant le hop1 (0x814d0f1)
main_calls = [v for a, k, v in events(MAIN, 0x814d0f1) if k == 'call']
for c in main_calls:
    fp = first_play(c)
    if fp is None:
        print("!! pas de premier play pour %x" % c, file=sys.stderr)
        continue
    for ans in correct(fp):
        emit(ans, "main-fastexit(%x) play(%d)" % (c, fp))

# --- hop1, hop2, hop3 : ladders
for f, stop in ((0x813d5dc, 0x8144ba9), (0x8144ba9, 0x8131f64), (0x8131f64, 0x810aab4)):
    lad = ladder(f, stop)
    print("%x : %d etages, dernier -> %x" % (f, len(lad), lad[-1][1] if lad else 0), file=sys.stderr)
    for N, callee in lad:
        for ans in wrong(N):
            emit(ans, "hop(%x) play(%d) WRONG" % (f, N))
        if callee != stop:
            fp = first_play(callee)
            if fp is None:
                print("!! pas de premier play pour fastexit %x" % callee, file=sys.stderr)
                continue
            for ans in correct(fp):
                emit(ans, "fastexit(%x) play(%d)" % (callee, fp))

# --- hop4 0x810aab4 : r == 5
for i in range(1, 5):
    emit(fizz(i), "hop4 play(46) correct i=%d" % i)
emit('x', "hop4 play(46) WRONG at 5 -> r=5")

# --- hop5 0x808ba1f : r == 1 -> fgets(348)
emit('x', "hop5 play(20) WRONG at 1 -> r=1 (fgets 0x15c)")

print("stream len:", len(stream), file=sys.stderr)
blob = b"".join(a.encode() + b"\n" for a in stream)
open('/tmp/bizz_stream.bin', 'wb').write(blob)
print("blob bytes:", len(blob), file=sys.stderr)
with open('/tmp/bizz_stream.txt', 'w') as fh:
    for a, tag in log:
        fh.write("%-12s %s\n" % (a, tag))
print("ok")
