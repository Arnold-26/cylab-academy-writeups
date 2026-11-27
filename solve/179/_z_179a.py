import sys, socket, time, re, struct, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# offsets libc
r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                    "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin && nm -D 179_libc.so.6 2>/dev/null | grep -iE ' (system|puts|read)@@' "],
                   capture_output=True, text=True)
print(r.stdout)
offs = {}
for line in r.stdout.splitlines():
    p = line.split()
    if len(p) >= 3:
        name = p[2].split("@")[0]
        offs[name] = int(p[0], 16)
print("offsets:", {k: hex(v) for k, v in offs.items()})
if "system" not in offs or "puts" not in offs:
    sys.exit(1)
