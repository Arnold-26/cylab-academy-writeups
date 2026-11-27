#!/usr/bin/env python3
import struct
fl = [8.191473375206089e-79, 3.775826202043335e+79, 1.1205295651588473e+253, 7.748604185565308e-304, 2.460307022775963e+257, 1.7734484618746183e-288, 4.089989556334856e+40, 1.7766596360849696e-302, 3.6509617888350745e+206, 4.1942076e-316]
b = b"".join(struct.pack("<d", x) for x in fl)
print(len(b), b.hex())
try:
    from pwn import disasm, context
    context.clear(arch='amd64')
    print(disasm(b))
except Exception as e:
    print("no pwntools disasm:", e)
