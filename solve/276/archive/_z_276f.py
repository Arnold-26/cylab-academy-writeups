import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "/tmp/cylab_eps/276_keygenme"
r = subprocess.run(["objdump", "-d", "-Mintel", P], capture_output=True, text=True).stdout
lines = r.split("\n")
targets = ("1230", "123a", "1252", "125c", "121d", "121f")
for i, l in enumerate(lines):
    if any(t in l for t in targets) and "#" in l:
        for j in range(max(0, i - 6), min(len(lines), i + 6)):
            print(lines[j])
        print("---")
