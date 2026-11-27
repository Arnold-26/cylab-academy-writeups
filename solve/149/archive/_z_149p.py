import subprocess, re
BIN = "/tmp/cylab_eps/149_checkpass"
PAT = re.compile(r"I\s+refs:\s+([\d,]+)")


def irefs(pw, reps=3):
    vals = []
    for _ in range(reps):
        r = subprocess.run(["valgrind", "--tool=cachegrind", "--cachegrind-out-file=/dev/null", BIN, pw],
                           capture_output=True, text=True)
        m = PAT.search(r.stderr)
        vals.append(int(m.group(1).replace(",", "")) if m else -1)
    return vals[0], vals


base = "academy{" + "A"*32 + "}"
known = "t1mingS1deChann3l_"
print("reference           :", irefs(base))
# increment progressif sur les 18 caracteres connus
for k in range(0, 19, 3):
    inner = known[:k] + "A" * (32 - k)
    pw = "academy{" + inner + "}"
    v, vals = irefs(pw)
    print("k=%2d (%r) -> %d  %s" % (k, known[:k], v, vals))
