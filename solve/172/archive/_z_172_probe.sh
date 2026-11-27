#!/bin/bash
cd /tmp/office
python3 - <<'EOF'
import subprocess
inp = b"1\nAlice\ny\n" + b"a"*28 + b"\n1000\n1234\nn\n3\n0\n"
p = subprocess.run(["./the_office"], input=inp, capture_output=True, timeout=10)
print("rc:", p.returncode)
print("--- stdout ---")
print(p.stdout.decode('latin-1'))
print("--- stderr ---")
print(p.stderr.decode('latin-1')[:800])
EOF
