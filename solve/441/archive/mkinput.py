import sys
from pwn import *
context.log_level = 'error'
context.arch = 'amd64'

# build a static input stream: sequence of ops
ops = []
def op(size, payload):
    ops.append(p64(size) + payload + b"\n")

# op0: alloc 0x10, ping
op(0x10, b"\x00"*8)
# op1: alloc 0x10, echo, payload 8 bytes to fill user area
op(0x10, b"\x01" + b"\x00"*7)

data = b"".join(ops)
open('./_z_441/input1.bin','wb').write(data)
print(len(data), data.hex())
