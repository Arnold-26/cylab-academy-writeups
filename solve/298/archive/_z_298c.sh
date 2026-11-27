#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 - <<'EOF'
import subprocess, time

def try_pin(pin, n=5):
    ts = []
    for _ in range(n):
        t0 = time.perf_counter()
        p = subprocess.run(["./298_pin_checker"], input=pin + "\n",
                           capture_output=True, text=True)
        ts.append(time.perf_counter() - t0)
    return sorted(ts)[len(ts) // 2]

known = ""
for pos in range(8):
    best = None
    for d in "0123456789":
        pin = known + d + "0" * (7 - len(known))
        t = try_pin(pin, 3)
        if best is None or t > best[1]:
            best = (d, t)
    known += best[0]
    print("prefixe:", known, "temps:", round(best[1] * 1000, 2), "ms")
print("PIN:", known)
p = subprocess.run(["./298_pin_checker"], input=known + "\n", capture_output=True, text=True)
print(p.stdout)
EOF
