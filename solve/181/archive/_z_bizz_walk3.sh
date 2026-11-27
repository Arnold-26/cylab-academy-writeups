#!/bin/bash
cd .
python3 - <<'EOF'
import subprocess, re
def fizz(n):
    if n % 15 == 0: return "FizzBuzz"
    if n % 3 == 0: return "Fizz"
    if n % 5 == 0: return "Buzz"
    return str(n)
inp = "".join(fizz(i) + "\n" for i in range(1, 30)).encode()
p = subprocess.run(["./_z_bizz"], input=inp, capture_output=True, timeout=10)
out = p.stdout.decode(errors="replace")
nums = re.findall(r"(\d+)\?", out)
print("len", len(out))
print("first prompts:", nums[:20])
print("distinct:", sorted(set(int(x) for x in nums))[:15])
print("tail:", out[-150:])
EOF
