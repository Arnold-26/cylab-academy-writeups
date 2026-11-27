#!/bin/bash
cd /tmp/office
python3 - <<'PY'
import subprocess
inp  = b"1\nA\ny\n" + b"a"*28 + b"\n1000\n111\nn\n"   # add A avec email 28
inp += b"2\n0\n"                                        # remove A
inp += b"1\nB\nn\n2000\n222\nn\n"                       # add B (sans email)
inp += b"1\nC\nn\n3000\n333\nn\n"                       # add C (sans email)
inp += b"3\n0\n"                                        # list + exit
p = subprocess.run(["./the_office"], input=inp, capture_output=True, timeout=10)
out = p.stdout.decode('latin-1')
print("rc:", p.returncode)
print(out)
PY
