import sys, re, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "nm -D --defined-only libc-2.27.so 2>/dev/null | awk '$2 ~ /[TWi]/ {print $1, $3}'"],
                     capture_output=True, text=True).stdout
cands = []
for line in out.splitlines():
    parts = line.split()
    if len(parts) < 2:
        continue
    try:
        off = int(parts[0], 16)
    except Exception:
        continue
    if off % 0x1000 == 0x8d0:
        cands.append((off, parts[1]))
print("symboles offset ≡ 0x8d0:", len(cands))
for off, name in cands[:25]:
    print("  0x%-8x %s" % (off, name))
