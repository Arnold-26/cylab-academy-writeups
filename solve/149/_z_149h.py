import sys, subprocess, re, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = "./149_checkpass"
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_re"
PREFIX = "academy{"
SUFFIX = "}"


def irefs(password):
    try:
        r = subprocess.run(["setarch", "-R", "valgrind", "--tool=cachegrind",
                            "--cachegrind-out-file=/dev/null", BIN, password],
                           capture_output=True, text=True, timeout=180, cwd=CWD)
    except Exception:
        return -1
    m = re.search(r"I\s+refs:\s+([\d,]+)", r.stderr or "")
    return int(m.group(1).replace(",", "")) if m else -1


base = PREFIX + "@" * 32 + SUFFIX
b0 = irefs(base)
print("baseline:", b0, flush=True)
chars = string.printable[:-6]
res = []
for c in chars:
    guess = PREFIX + c + "@" * 31 + SUFFIX
    v = irefs(guess)
    res.append((v, c))
orig = PREFIX + "@" * 32 + SUFFIX
for v, c in sorted(res, reverse=True)[:8]:
    print(f"  {c!r} -> {v}  (delta {v - b0})", flush=True)
