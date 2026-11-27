import sys, re, json, ast
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from fpylll import IntegerMatrix, LLL, BKZ

txt = open("/tmp/cylab_711/public.txt").read()
N = int(re.search(r"N = (\d+)", txt).group(1))
p = int(re.search(r"p = (\d+)", txt).group(1))
q = int(re.search(r"q = (\d+)", txt).group(1))
h = ast.literal_eval(re.search(r"h = (\[[^\]]*\])", txt).group(1))
ct = ast.literal_eval(re.search(r"ct = (\[\[.*\]\])", txt, re.S).group(1))
print("N,p,q:", N, p, q, "h:", len(h), "ct:", len(ct))

# matrice circulante H avec H[i][j] = h[(i-j) % N]
def build():
    A = IntegerMatrix(2 * N, 2 * N)
    for i in range(N):
        for j in range(N):
            A[i, j] = 1 if i == j else 0
            A[i, N + j] = h[(i - j) % N]
    for i in range(N):
        for j in range(N):
            A[N + i, j] = 0
            A[N + i, N + j] = q if i == j else 0
    return A

A = build()
LLL.reduction(A)
BKZ.reduction(A, BKZ.Param(block_size=30))
print("reduction faite")

def poly_mul(a, b):
    r = [0] * N
    for i in range(N):
        if a[i] == 0:
            continue
        for j in range(N):
            r[(i + j) % N] += a[i] * b[j]
    return r

best = None
for k in range(A.nrows):
    row = [A[k, j] for j in range(2 * N)]
    f = row[:N]
    g = row[N:]
    if all(x in (-1, 0, 1) for x in f) and any(x != 0 for x in f):
        # verifier f*h = p*g (mod q)
        prod = poly_mul(f, h)
        ok = all((prod[i] - p * g[i]) % q == 0 for i in range(N))
        if ok:
            best = (f, g)
            print("TROUVE f:", f[:10], "coeffs:", set(f))
            break
if not best:
    print("pas trouve par la reduction, essai de verification partielle")
    for k in range(min(20, A.nrows)):
        row = [A[k, j] for j in range(2 * N)]
        f = row[:N]
        print(k, "norme f:", sum(x * x for x in f), "max:", max(abs(x) for x in f))
else:
    f = best[0]
    print("f =", f)
