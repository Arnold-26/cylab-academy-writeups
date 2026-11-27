import sys, re, ast, itertools
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from fpylll import IntegerMatrix, LLL, BKZ

txt = open("/tmp/cylab_711/public.txt").read()
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
        for j in range(N):
            A[i, j] = 1 if i == j else 0
            A[i, N + j] = h[(i - j) % N]
    for i in range(N):
        A[N + i, N + i] = q
    return A

A = build()
LLL.reduction(A)
BKZ.reduction(A, BKZ.Param(block_size=30))

def lift(a):
    return [x - q if x > q // 2 else x for x in a]

def tries(f):
    # inverse de f mod p
    # f_p_inv : on resout f * inv = 1 mod p via algèbre lineaire sur Z_p
    # methode simple : recherche par force brute sur les polynomes ? non.
    # On utilise le fait que m = f*c mod q leve, puis mod p : m = (f*c)/p ??? non.
    # NTRU : a = f*c mod q (centre), m = f_p_inv * a mod p
    # calcul de f_p_inv via l'algorithme d'Euclide polynomial sur Z_p
    def poly_mod(a, b, mod):
        a = [x % mod for x in a]
        b = [x % mod for x in b]
        while len(b) > 1 and b[-1] == 0:
            b.pop()
        while len(a) >= len(b) and any(a):
            if a[-1] == 0:
                a.pop()
                continue
            coef = a[-1] * pow(b[-1], -1, mod) % mod
            shift = len(a) - len(b)
            for i in range(len(b)):
                a[i + shift] = (a[i + shift] - coef * b[i]) % mod
            while len(a) > 1 and a[-1] == 0:
                a.pop()
        return a
    # trop complexe ; on passe par un systeme lineaire mod p
    import numpy as np
    # matrice de multiplication par f mod p (circulante)
    M = [[f[(i - j) % N] % p for j in range(N)] for i in range(N)]
    # resoudre M * inv = e_0 mod p
    import copy
    A2 = [[(M[i][j]) % p for j in range(N)] + [1 if i == 0 else 0] for i in range(N)]
    for col in range(N):
        piv = next((r for r in range(col, N) if A2[r][col] % p), None)
        if piv is None:
            return None
        A2[col], A2[piv] = A2[piv], A2[col]
        inv = pow(A2[col][col], -1, p)
        A2[col] = [(x * inv) % p for x in A2[col]]
        for r in range(N):
            if r != col and A2[r][col] % p:
                fac = A2[r][col] % p
                A2[r] = [(A2[r][c] - fac * A2[col][c]) % p for c in range(N + 1)]
    return [A2[i][N] % p for i in range(N)]

results = []
for k in range(min(40, A.nrows)):
    row = [A[k, j] for j in range(2 * N)]
    f = row[:N]
    if not all(x in (-1, 0, 1) for x in f) or not any(f):
        continue
    finv = tries(f)
    if finv is None:
        continue
    # verifier f * finv = 1 mod p
    chk = poly_mul(f, finv, p)
    if chk[0] % p != 1 or any(chk[i] % p for i in range(1, N)):
        continue
    # dechiffrer le premier bloc
    c = ct[0]
    a = lift(poly_mul(f, c, q))
    m = [x % p for x in poly_mul(finv, a, p)]
    bits = "".join(str(b) for b in m)
    chars = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits) - 7, 8))
    print(k, "->", chars[:40])
    if "academy" in chars or "pico" in chars:
        results.append((f, finv, chars))
        break
print("trouve:", bool(results))
