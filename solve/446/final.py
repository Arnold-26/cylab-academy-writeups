import sys
sys.path.insert(0, '/mnt/d/ctf-index/_z_446')
from _z_446_solve import SEQ, run_remote, run_local

print('len:', len(SEQ))
print('repr:', repr(SEQ))
print('hex :', SEQ.hex())
print()
# reproducibility check on the live remote
out = run_remote(SEQ)
s = out.decode('latin1', 'replace')
import re
flag = re.findall(r'(?:academy|picoCTF)\{[^}\n]*\}', s)
print('remote bytes:', len(out), 'flag:', flag)
for line in s.splitlines():
    if 'academy{' in line or 'picoCTF{' in line:
        print('FLAG LINE:', repr(line))
