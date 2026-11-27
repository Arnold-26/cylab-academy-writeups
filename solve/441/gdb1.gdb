set pagination off
set confirm off
python
import gdb, struct
hits = [0]
class BP(gdb.Breakpoint):
    def stop(self):
        hits[0] += 1
        rdi = int(gdb.parse_and_eval("$rdi"))
        fs = int(gdb.parse_and_eval("$fs_base"))
        gdb.write("=== GETS#%d rdi(buf)=%#x fs_base=%#x\n" % (hits[0], rdi, fs))
        return hits[0] >= 2
BP("gets")
end
run < ./_z_441/input1.bin
info proc mappings
x/8gx $fs_base-0x100
