import struct
data = open('/tmp/winadb/u300.exe', 'rb').read()


def off(v):
    return 0x400 + (v - 0x401000)


for v in (0x401073, 0x4011e0, 0x40122b, 0x40127b, 0x401195):
    b = data[off(v):off(v) + 5]
    rel = struct.unpack('<i', b[1:5])[0]
    print("thunk @%#x -> %#x" % (v, v + 5 + rel))
