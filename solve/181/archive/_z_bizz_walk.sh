#!/bin/bash
cd .
python3 - <<'EOF'
import subprocess
inp = b""
for _ in range(120):
    inp += b"1\n2\n3\n"
p = subprocess.run(["./_z_bizz"], input=inp, capture_output=True, timeout=10)
out = p.stdout.decode(errors="replace")
print("len", len(out))
print("HEAD:", out[:120])
print("TAIL:", out[-300:])
import re
nums = re.findall(r"(\d+)\?", out)
print("distinct prompts:", sorted(set(nums), key=int)[:20])
print("count prompts:", len(nums))
EOF
