import subprocess, os, re, time, select, sys
from _z_446_solve import SEQ

here = os.path.dirname(os.path.abspath(__file__))
p = subprocess.Popen(['./game'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, cwd=here, bufsize=0)
fd = p.stdout.fileno()
buf = bytearray()

def pump(t=0.35):
    t0 = time.time()
    got = 0
    while time.time() - t0 < t:
        r, _, _ = select.select([fd], [], [], 0.05)
        if r:
            c = os.read(fd, 65536)
            if not c:
                return got, True
            buf.extend(c); got += len(c)
            t = 0.05  # got data: shorten remaining wait
        elif p.poll() is not None:
            return got, True
    return got, False

def nprint():
    return buf.count(b'Lives left')

# initial map
pump(0.6)
print('initial maps', nprint())
prev = nprint()
trace = []
for i, b in enumerate(SEQ):
    try:
        p.stdin.write(bytes([b])); p.stdin.flush()
    except Exception as e:
        print('write failed at', i, e); break
    before = nprint()
    got, dead = pump(0.4)
    now = nprint()
    s = buf.decode('latin1')
    lev = re.findall(r'Level: (-?\d+)', s)
    liv = re.findall(r'Lives left: (-?\d+)', s)
    pos = re.findall(r'Player position: (-?\d+) (-?\d+)', s)
    trace.append((i, b, now - before, lev[-1] if lev else None, liv[-1] if liv else None, pos[-1] if pos else None, dead))
    print(f'{i:3d} {bytes([b])!r:8s} prints={now-before} level={lev[-1] if lev else None:>4} lives={liv[-1] if liv else None:>12} pos={pos[-1] if pos else None} dead={dead}')
    if dead:
        tail = s[-200:].replace('\n', '\\n')
        print('END tail:', tail)
        break
try: p.kill()
except Exception: pass
