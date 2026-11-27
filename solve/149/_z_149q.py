import subprocess, re, string, sys

BIN = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/149_checkpass"
PAT = re.compile(r"I\s+refs:\s+([\d,]+)")
CHARS = string.ascii_lowercase + string.digits + "_" + string.ascii_uppercase
known = "t1mingS1deChann3l_"
POS = int(sys.argv[1]) if len(sys.argv) > 1 else 18


def irefs(pw):
    r = subprocess.run(["valgrind", "--tool=cachegrind", "--cachegrind-out-file=/dev/null", BIN, pw],
                       capture_output=True, text=True)
    m = PAT.search(r.stderr)
    return int(m.group(1).replace(",", "")) if m else -1


res = []
for ch in CHARS:
    inner = (known + ch)[:POS+1]
    inner = inner + "A" * (32 - len(inner))
    pw = "academy{" + inner + "}"
    n = irefs(pw)
    res.append((n, ch))
res.sort(reverse=True)
print("position", POS, "- top 8 par Irefs:")
for n, ch in res[:8]:
    print("   %r -> %d" % (ch, n))
print("min:", res[-1])
