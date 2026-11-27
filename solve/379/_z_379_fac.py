import subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sympy

ct, dval = [int(x) for x in open("/mnt/d/ctf-index/_z_379_data.txt").read().split()]
K = 65537 * dval - 1
print("K bits:", K.bit_length())


def ecm_factor(n, b1, curves, timeout=60):
    try:
        r = subprocess.run(["ecm", "-c", str(curves), str(b1)], input=str(n).encode(),
                           capture_output=True, timeout=timeout)
        out = r.stdout.decode()
        for line in out.split("\n"):
            line = line.strip()
            if line and line.split()[0].isdigit() and "Found" not in line:
                f = int(line.split()[0])
                if 1 < f < n and n % f == 0:
                    return f
    except subprocess.TimeoutExpired:
        print("   (timeout ecm)")
    return None


rem = K
found = {}
t0 = time.time()
for b1, curves in ((2000, 25), (11000, 40), (50000, 40), (250000, 30)):
    while True:
        if rem == 1 or sympy.isprime(rem):
            break
        f = ecm_factor(rem, b1, curves, timeout=90)
        if not f:
            break
        print("  facteur %d bits trouve (B1=%d) apres %.0fs" % (f.bit_length(), b1, time.time() - t0), flush=True)
        # factorise f completement
        for p, e in sympy.factorint(f).items():
            found[p] = found.get(p, 0) + e
        rem //= f
    if rem == 1 or sympy.isprime(rem):
        break
print("temps total %.0fs" % (time.time() - t0))
if rem > 1:
    if sympy.isprime(rem):
        found[rem] = found.get(rem, 0) + 1
        rem = 1
print("reste:", rem, "bits", rem.bit_length() if rem > 1 else 0)
for p, e in sorted(found.items()):
    print("   %d^%d  (%d bits)" % (p, e, p.bit_length()))
import json
json.dump({"factors": {str(p): e for p, e in found.items()}, "rest": str(rem)}, open("/mnt/d/ctf-index/_z_379_fac.json", "w"))
