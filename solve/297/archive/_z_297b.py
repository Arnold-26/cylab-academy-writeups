import hashlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("53c1beea6e427b3de1acf4834baed794f4bbd0dfb2db5f682edda3952b")
MOD = 10 ** 10000

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
P = matpow(M, n - 3, MOD)
sol = (P[0][0] * 4 + P[0][1] * 3 + P[0][2] * 2 + P[0][3] * 1) % MOD
s = str(sol)
print("taille:", len(s))
md5 = hashlib.md5(s.encode()).hexdigest()
print("md5:", md5, "| attendu:", VERIF_KEY, "|", md5 == VERIF_KEY)
if md5 == VERIF_KEY:
    key = hashlib.sha256(s.encode()).digest()
    flag = bytes([c ^ key[i] for i, c in enumerate(ENCRYPTED_FLAG)]).decode()
    print("FLAG:", flag)
