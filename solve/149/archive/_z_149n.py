import subprocess, string, sys, re

BIN = "/tmp/cylab_eps/149_checkpass"
CHARS = string.ascii_lowercase + string.digits + "_" + string.ascii_uppercase
PREFIX = sys.argv[1] if len(sys.argv) > 1 else "academy{"
LOG = "/tmp/checkpass_progress.txt"
PAT = re.compile(r"I\s+refs:\s+([\d,]+)")


def irefs(pw):
    r = subprocess.run(["valgrind", "--tool=cachegrind", "--cachegrind-out-file=/dev/null", BIN, pw],
                       capture_output=True, text=True)
    m = PAT.search(r.stderr)
    return int(m.group(1).replace(",", "")) if m else -1


known = ""
open(LOG, "w").write("=== prefixe %s, alphabet %d ===\n" % (PREFIX, len(CHARS)))
for pos in range(32):
    best, bestc = -1, None
    for ch in CHARS:
        inner = known + ch + "A" * (31 - pos)
        n = irefs(PREFIX + inner + "}")
        if n > best:
            best, bestc = n, ch
    known += bestc
    with open(LOG, "a") as f:
        f.write("pos %2d -> %r  (Irefs=%d)  inner=%r\n" % (pos, bestc, best, known))
    print("pos %2d -> %r (Irefs=%d) inner=%r" % (pos, bestc, best, known), flush=True)
print("MOT DE PASSE:", PREFIX + known + "}")
