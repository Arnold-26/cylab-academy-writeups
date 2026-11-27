import sys, time
from pwn import *
context.log_level = 'error'
p = process(['./ld-2.23.so', '--library-path', '.', './sice_cream'], stderr=process.STDOUT)
print("pid", p.pid)
for ln in open('/proc/%d/maps' % p.pid).read().split('\n'):
    if 'sice' in ln or 'heap' in ln or 'libc' in ln:
        print("  ", ln)
buf = bytearray(b'A' * 0x100)
buf[0x18:0x20] = p64(0x91)
p.recvuntil(b'Whats your name?'); p.recvuntil(b'> '); p.send(bytes(buf))
def buy(size, data):
    p.recvuntil(b'> '); p.send(b'1\n')
    p.recvuntil(b'> '); p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> '); p.send(data)
    p.recvuntil(b'Here you go!')
buy(0x58, b'A' * 0x58)
print("--- apres un malloc:")
for ln in open('/proc/%d/maps' % p.pid).read().split('\n'):
    if 'heap' in ln:
        print("  ", ln)
p.close()
