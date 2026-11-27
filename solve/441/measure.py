import gdb, struct

OPS = [
    (0x10, b"\x00"*8),
    (0x10, b"\x01" + b"\x00"*7),
    (0x10, b"\x00"*8),
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
        try:
            sz = int(gdb.parse_and_eval("*(unsigned long*)%#x" % pkt))
        except Exception:
            sz = -1
        gdb.write("GETS#%d pkt=%#x chunkhdr=%#x pkt->sz=%#x\n" % (hits[0], pkt, pkt-0x10, sz))
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
gdb.write("\nfs_base = %#x\n" % fs)
gdb.write("\n---- 0x80 qwords below fs_base ----\n")
gdb.write(gdb.execute("x/48gx %#x" % (fs - 0x180), to_string=True))
heap = None
try:
    heap = int(gdb.parse_and_eval("(unsigned long)$heap")) if False else None
except Exception:
    pass
