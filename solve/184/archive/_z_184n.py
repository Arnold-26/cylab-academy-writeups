import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"/tmp/cylab_eps"
gdb = """set pagination off
run < in184c.bin
printf "EIP=%p\\n", $eip
info registers eax ebx ecx edx edi esp
x/8i $eip
quit
"""
open(CWD + r"\g184c.gdb", "w").write(gdb)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "gdb -nx -q -batch -x g184c.gdb ./184_fun 2>&1 | tail -22"],
                     capture_output=True, text=True).stdout
print(out)
