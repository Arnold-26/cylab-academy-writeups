#!/bin/bash
cd /tmp/office
python3 - <<'PY'
import subprocess
for label, inp in [
    ("4 seul", b"4\n0\n"),
    ("add puis 4", b"1\nBob\nn\n1000\n111\nn\n4\n0\n"),
]:
    p = subprocess.run(["./the_office"], input=inp, capture_output=True, timeout=10)
    print("=====", label, "rc:", p.returncode)
    print("STDOUT:", p.stdout.decode('latin-1').replace("\n", "\\n")[:500])
    print("STDERR:", p.stderr.decode('latin-1')[:300])
PY
