import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/276_keygenme"
r = subprocess.run(["objdump", "-d", "-Mintel", P], capture_output=True, text=True).stdout
lines = r.split("\n")
print("instructions:", len(lines))
# afficher les references aux adresses des morceaux (0x1230-0x1270)
for i, l in enumerate(lines):
    if any(f"#{a}" in l for a in range(0x1210, 0x1290, 1)):
        for j in range(max(0, i - 4), min(len(lines), i + 5)):
            print(lines[j])
        print("---")
