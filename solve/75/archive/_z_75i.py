import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"/tmp/cylab_eps"
setup = ("cd /tmp/cylab_eps && "
         "cp -f 75_ld-2.29.so ld-2.29.so && cp -f 75_libc.so.6 libc.so.6 && "
         "chmod +x ld-2.29.so && ls -la ld-2.29.so libc.so.6")
print(subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c", setup],
                     capture_output=True, text=True).stdout)
open(CWD + r"\in75.txt", "w").write("y\n3\n")
gdb = """set pagination off
break *0x400d3c
run < in75.txt
printf "valeur [0x601fe8] = %p\\n", *(void**)0x601fe8
info proc mappings
quit
"""
open(CWD + r"\g75b.gdb", "w").write(gdb)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "gdb -nx -q -batch -x g75b.gdb ./75_zero_to_hero 2>&1 | head -26"],
                     capture_output=True, text=True).stdout
print(out[:2200])
