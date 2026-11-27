# 297 - Sequences  (Cryptography, picoCTF 2022)
# Flag: academy{b1g_numb3rs_f5b03a75}
# Write-up: ../../../writeups/cryptography/297-sequences.md
# This is the script that produced the flag; historical variants are in archive/.
#
import hashlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("53c1beea6e427b3de1acf4834baed794f4bbd0dfb2db5f682edda3952b")
MOD = 10 ** 10000

# verification de la petite valeur
def brute(i):
    m = [1, 2, 3, 4]
    if i < 4:
        return m[i]
    for k in range(4, i + 1):
        m.append(55692 * m[k - 4] - 9549 * m[k - 3] + 301 * m[k - 2] + 21 * m[k - 1])
    return m[i]

print("m(4) =", brute(4), "| m(5) =", brute(5))

M = [
    [21, 301, -9549, 55692],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
]


def matmul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            a = Ai[k]
            if a:
                Bk = B[k]
                for j in range(n):
                    Ci[j] = (Ci[j] + a * Bk[j]) % mod
    return C


def matpow(A, e, mod):
    n = len(A)
    R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in A]
    while e:
        if e & 1:
            R = matmul(R, base, mod)
        base = matmul(base, base, mod)
        e >>= 1
    return R


n = ITERS
exp = n - 3
P = matpow(M, exp, MOD)
v = [4, 3, 2, 1]
sol = sum(P[0][i] * v[i] for i in range(4)) % MOD
print("taille du resultat:", len(str(sol)))
md5 = hashlib.md5(str(sol).encode()).hexdigest()
print("md5:", md5, "attendu:", VERIF_KEY, "->", md5 == VERIF_KEY)
if md5 == VERIF_KEY:
    key = hashlib.sha256(str(sol).encode()).digest()
    flag = bytes([c ^ key[i] for i, c in enumerate(ENCRYPTED_FLAG)]).decode()
    print("FLAG:", flag)
