import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\143_gauntlet"
d = open(p, "rb").read()
print("taille:", len(d))
# .text ~ 0x1000..0x1300 ; on cherche des gadgets utiles dans tout le fichier executable
import re
for name, pat in (("jmp rsp (ff e4)", b"\xff\xe4"),
                  ("call rsp (ff d4)", b"\xff\xd4"),
                  ("push rsp; ret (54 c3)", b"\x54\xc3"),
                  ("jmp rax (ff e0)", b"\xff\xe0"),
                  ("call rax (ff d0)", b"\xff\xd0")):
    idxs = [m.start() for m in re.finditer(re.escape(pat), d)]
    print("%-22s -> %d %s" % (name, len(idxs), idxs[:6]))
# verifier la section executable
import subprocess
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "readelf", "-SW",
                      "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/143_gauntlet"],
                     capture_output=True, text=True).stdout
for line in out.splitlines():
    if ".text" in line or ".init" in line or ".plt" in line or ".fini" in line:
        print(line.strip())
