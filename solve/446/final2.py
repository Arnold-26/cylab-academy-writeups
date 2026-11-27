import sys, re, time
sys.path.insert(0, '/mnt/d/ctf-index/_z_446')
from _z_446_solve import SEQ, run_remote

for attempt in (1, 2):
    t0 = time.time()
    out = run_remote(SEQ, timeout=60)
    s = out.decode('latin1', 'replace')
    lev = re.findall(r'Level: (-?\d+)', s)
    flag = re.findall(r'(?:academy|picoCTF)\{[^}\n]*\}', s)
    print(f'attempt {attempt}: bytes={len(out)} maps={len(lev)} levels={sorted(set(lev))} flag={flag} dt={time.time()-t0:.1f}s')
    print('  tail:', repr(s[-160:]))
