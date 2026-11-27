import subprocess, string, sys, json, os

BIN = "/tmp/cylab_eps/149_checkpass"
CHARS = [c for c in string.printable if c not in "\t\n\r\x0b\x0c"]
PREFIX = sys.argv[1] if len(sys.argv) > 1 else "academy{"
LOG = "/tmp/checkpass_progress.txt"


def irefs(pw):
    r = subprocess.run(["valgrind", "--tool=cachegrind", "--cachegrind-out-file=/dev/null", BIN, pw],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "I   refs:" in line:
            return int(line.split(":")[1].replace(",", "").strip())
    return -1


known = ""
with open(LOG, "a") as f:
    f.write("=== debut prefixe %s ===\n" % PREFIX)
for pos in range(32):
    best, bestc = -1, None
    for ch in CHARS:
        inner = known + ch + "A" * (31 - pos)
        pw = PREFIX + inner + "}"
        n = irefs(pw)
        if n > best:
            best, bestc = n, ch
    known += bestc
    with open(LOG, "a") as f:
        f.write("pos %2d -> %r  (Irefs=%d)  inner=%r\n" % (pos, bestc, best, known))
    print("pos %2d -> %r  inner=%r" % (pos, bestc, known), flush=True)
print("MOT DE PASSE:", PREFIX + known + "}")
