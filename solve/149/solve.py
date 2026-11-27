# 149 - Checkpass  (Reverse Engineering, picoCTF 2021)
# Flag: academy{...}
# Write-up: ../../../writeups/reverse-engineering/149-checkpass.md
# Script exact utilise pour produire le flag.
#
import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BIN = "./149_checkpass"
CWD = "/tmp/cylab_re"
PREFIX = "academy{"
SUFFIX = "}"
INNER = 32


def irefs(password):
    try:
        r = subprocess.run(["setarch", "-R", "valgrind", "--tool=cachegrind",
                            "--cachegrind-out-file=/dev/null", BIN, password],
                           capture_output=True, text=True, timeout=180, cwd=CWD)
    except Exception:
        return -1
    m = re.search(r"I\s+refs:\s+([\d,]+)", r.stderr or "")
    if not m:
        return -1
    return int(m.group(1).replace(",", ""))


charset = "0123456789abcdef_"
flag = list("@" * INNER)
best = irefs(PREFIX + "".join(flag) + SUFFIX)
print("baseline:", best, flush=True)
for pos in range(INNER):
    cands = sorted(charset, key=lambda c: 0)
    found = None
    for c in cands:
        guess = flag[:]
        guess[pos] = c
        val = irefs(PREFIX + "".join(guess) + SUFFIX)
        if val > best:
            best = val
            flag[pos] = c
            found = c
            print(f"pos {pos}: {c} -> {PREFIX}{''.join(flag)}{SUFFIX} (refs={val})", flush=True)
            break
    if found is None:
        print(f"pos {pos}: aucun candidat (charset epuise)", flush=True)
        break
print("FINAL:", PREFIX + "".join(flag) + SUFFIX, flush=True)
