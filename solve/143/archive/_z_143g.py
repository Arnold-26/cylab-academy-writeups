import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"/tmp/cylab_eps"
fmt = ".".join(["%p"] * 40)
open(CWD + r"\in143.txt", "w").write(fmt + "\n" + "AAAA\n")
gdb_script = """set pagination off
break *0x40124f
run < in143.txt
printf "buf = %p\\n", $rbp-0x70
printf "rbp = %p\\n", $rbp
quit
"""
open(CWD + r"\g143.gdb", "w").write(gdb_script)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "gdb -nx -q -batch -x g143.gdb ./143_gauntlet 2>&1 | head -25"],
                     capture_output=True, text=True).stdout
print(out)
