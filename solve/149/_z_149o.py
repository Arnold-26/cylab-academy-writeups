import subprocess, re
BIN = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/149_checkpass"
PAT = re.compile(r"I\s+refs:\s+([\d,]+)")


def irefs(pw):
    r = subprocess.run(["valgrind", "--tool=cachegrind", "--cachegrind-out-file=/dev/null", BIN, pw],
                       capture_output=True, text=True)
    m = PAT.search(r.stderr)
    out = r.stdout.strip().splitlines()
    return (int(m.group(1).replace(",", "")) if m else -1), (out[-1] if out else "")


cases = [
    ("academy{" + "a"*32 + "}", "academy a..."),
    ("academy{" + "t"*32 + "}", "academy t..."),
    ("picoCTF{" + "a"*32 + "}", "picoCTF a..."),
    ("picoCTF{" + "t"*32 + "}", "picoCTF t..."),
    ("academy{" + "t1mingS1deChann3l_" + "A"*14 + "}", "inner connu debut"),
    ("academy{" + "a"*32 + "}", "reference a"),
]
for pw, label in cases:
    n, out = irefs(pw)
    print("%-22s Irefs=%-10d sortie=%r" % (label, n, out))
