import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
open(CWD + r"\in75.txt", "w").write("y\n3\n")
gdb = """set pagination off
break *0x400d3c
run < in75.txt
printf "valeur [0x601fe8] = %p\\n", *(void**)0x601fe8
info proc mappings
quit
"""
open(CWD + r"\g75.gdb", "w").write(gdb)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "chmod +x 75_zero_to_hero 75_ld-2.29.so 2>/dev/null; "
                      "gdb -nx -q -batch -x g75.gdb ./75_zero_to_hero 2>&1 | head -30"],
                     capture_output=True, text=True).stdout
print(out[:2000])
