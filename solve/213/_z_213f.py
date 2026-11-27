import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
gdb = """set pagination off
run < in213.bin
printf "EIP=%p\\n", $eip
info registers rax rbx rcx r12 rsp
x/8i $eip
printf "rsp-16:\\n"
x/8gx $rsp
quit
"""
open(CWD + r"\g213.gdb", "w").write(gdb)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "gdb -nx -q -batch -x g213.gdb ./213_chall 2>&1 | tail -22"],
                     capture_output=True, text=True).stdout
print(out)
