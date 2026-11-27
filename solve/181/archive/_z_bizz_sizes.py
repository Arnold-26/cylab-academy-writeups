import re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = subprocess.run(["objdump", "-d", "-M", "intel", "./_z_bizz"],
                     capture_output=True, text=True).stdout
lines = out.splitlines()
sizes = []
for i, ln in enumerate(lines):
    if "call" in ln and "fgets@plt" in ln:
        # remonter jusqu'au push immediat de taille
        for j in range(i - 1, max(0, i - 6), -1):
            m = re.search(r"push\s+0x([0-9a-f]+)", lines[j])
            if m:
                sizes.append((int(m.group(1), 16), ln.split(":")[0].strip()))
                break
print("fgets sizes:", sorted(sizes, reverse=True))
