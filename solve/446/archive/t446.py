import subprocess, os, sys
def run(seq, timeout=60):
    p = subprocess.run(["./game"], input=seq, capture_output=True, timeout=timeout)
    out = p.stdout
    return out
# route test: row 1 -> col -1 -> row 0 -> col -19 (level LSB)
seq = b"w"*3 + b"a"*5 + b"w" + b"a"*18
out = run(seq)
txt = out.decode("latin1", "replace")
print("obstacle:", "obstacle" in txt, "| lives:", txt.count("Lives left"))
import re
m = re.findall(r"Player position: (\d+) (\d+)", txt)
print("last pos:", m[-1] if m else None, "n_print:", len(m))
print(txt.splitlines()[-3:] if False else "")
