import sys, re, ast
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from fpylll import IntegerMatrix, LLL, BKZ

txt = open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_711/public.txt").read()
N = int(re.search(r"N = (\d+)", txt).group(1))
p = int(re.search(r"p = (\d+)", txt).group(1))
q = int(re.search(r"q = (\d+)", txt).group(1))
h = ast.literal_eval(re.search(r"h = (\[[^\]]*\])", txt).group(1))
ct = ast.literal_eval(re.search(r"ct = (\[\[.*\]\])", txt, re.S).group(1))


def poly_mul(a, b, mod=None):
    r = [0] * N
    for i in range(N):
        if a[i] == 0:
            continue
        ai = a[i]
        for j in range(N):
            r[(i + j) % N] += ai * b[j]
    if mod:
        r = [x % mod for x in r]
    return r


def build():
    A = IntegerMatrix(2 * N, 2 * N)
    for i in range(N):
        A[i, i] = 1
        for k in range(N):
            A[i, N + k] = h[(k - i) % N]
    for i in range(N):
        A[N + i, N + i] = q
    return A


A = build()
LLL.reduction(A)
BKZ.reduction(A, BKZ.Param(block_size=30))
print("reduction ok")

found = None
for k in range(A.nrows):
    row = [A[k, j] for j in range(2 * N)]
    f = row[:N]
    g = row[N:]
    if not all(x in (-1, 0, 1) for x in f) or not any(f):
        continue
    prod = poly_mul(f, h)
    if all((prod[i] - p * g[i]) % q == 0 for i in range(N)):
        found = (f, g)
        print("TROUVE f (ligne", k, "):", f)
        break
print("trouve:", found is not None)
if found:
    f = found[0]
    # inverse de f mod p par systeme lineaire
    M = [[f[(i - j) % N] % p for j in range(N)] for i in range(N)]
    A2 = [[M[i][j] % p for j in range(N)] + [1 if i == 0 else 0] for i in range(N)]
    for col in range(N):
        piv = next((r for r in range(col, N) if A2[r][col] % p), None)
        if piv is None:
            print("pas inversible")
            sys.exit()
        A2[col], A2[piv] = A2[piv], A2[col]
        inv = pow(A2[col][col], -1, p)
        A2[col] = [(x * inv) % p for x in A2[col]]
        for r in range(N):
            if r != col and A2[r][col] % p:
                fac = A2[r][col] % p
                A2[r] = [(A2[r][c] - fac * A2[col][c]) % p for c in range(N + 1)]
    finv = [A2[i][N] % p for i in range(N)]
    out = ""
    for c in ct:
        a = [x % q for x in poly_mul(f, c)]
        a = [x - q if x > q // 2 else x for x in a]
        m = [x % p for x in poly_mul(finv, a, p)]
        bits = "".join(str(b) for b in m)
        out += "".join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits) - 7, 8))
    print("MESSAGE:", out)
