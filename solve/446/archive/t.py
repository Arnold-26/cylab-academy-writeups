import subprocess, re, sys, os, select, time, signal

GAME = './game'

def run(seq, maxbytes=400000, timeout=15.0, kill_after=True):
    """Feed seq, keep stdin open (avoid EOF loop), read bounded output."""
    p = subprocess.Popen([GAME], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, cwd=os.path.dirname(os.path.abspath(__file__)))
    try:
        p.stdin.write(seq)
        p.stdin.flush()
    except Exception:
        pass
    out = bytearray()
    t0 = time.time()
    fd = p.stdout.fileno()
    while time.time() - t0 < timeout and len(out) < maxbytes:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            out += chunk
            if b'FLAG' in out or b'academy{' in out:
                break
        else:
            if p.poll() is not None:
                break
    if kill_after:
        try:
            p.kill()
        except Exception:
            pass
    try:
        p.wait(timeout=2)
    except Exception:
        pass
    return bytes(out), p.returncode

def report(seq, **kw):
    out, rc = run(seq, **kw)
    s = out.decode('latin1')
    pos = re.findall(r'Player position: (-?\d+) (-?\d+)', s)
    lev = re.findall(r'Level: (-?\d+)', s)
    liv = re.findall(r'Lives left: (-?\d+)', s)
    flag = re.findall(r'(?:academy|picoCTF|FLAG)\{[^}]*\}', s)
    print('rc', rc, 'npos', len(pos), 'bytes', len(out))
    print('positions', pos[:40])
    print('levels', lev[:40])
    print('lives', liv[:40])
    print('flag', flag[:5])
    for m in ('You win', 'obstacle', 'Game over', 'Next level'):
        if m in s:
            print('MARKER:', m)
    return s

if __name__ == '__main__':
    # model check: walk to (0,-1) then to (0,-4); lives byte3 should become '@'=0x40
    seq = b'www' + b'a'*5 + b'w' + b'aaa'
    report(seq)
