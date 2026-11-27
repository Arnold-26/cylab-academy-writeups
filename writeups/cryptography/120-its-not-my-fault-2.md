# 120 — It's Not My Fault 2 — Cryptography

**Flag :** `academy{p0lyn0m14l_4r17hm371c_73chn1qu35_4r3_u53ful_1n_m4ny_f13ld5!!!}`
**Cible :** `nc chatelaine.cylabacademy.net <port>` + source `not_my_fault_again.py`

## Le service (source)

```python
# PoW : input commencant par 5 chiffres, md5 finissant par 6 hexdigits donnes
p, q = getPrime(512), getPrime(512)          # GCD(p-1,q-1) == 2
print("Public Modulus : ", n)                # n = p*q
d_p = random.randint(1, 1 << 36)             # <-- 36 bits !
d_q = random.randint(1, q-1)
d   = CRT(d_p mod p-1, d_q mod q-1)
e   = inverse(d, (p-1)*(q-1))
print("Clue : ", e)
ans = int(input())                            # 15 minutes
if ans == p + q: print(FLAG)
```

On ne recoit que `n` et `e`, mais on sait que **`d_p = d mod (p-1)` est < 2^36**. Attaque
« petit exposant CRT » (Galbraith, *Mathematics of Public Key Cryptography* p. 529 ;
Koszegi) : ce n'est **pas** une attaque par faute.

## L'attaque

`e·d_p ≡ 1 (mod p-1)`, donc pour tout `m` : `p | m^(e·d_p-1) - 1`.

Écrire `d_p = a·L + b` avec `0 ≤ a,b < L` (`L = 2^18`, `L² = 2^36`). Alors

```
m^(e(aL+b)-1) - 1 = v_b · u^a - 1     avec  v_b = m^(e·b-1) mod n,  u = m^(e·L) mod n
```

Poser `P(x) = Π_{b=0}^{L-1} (v_b·x - 1) mod n`. Pour le bon `a`, le facteur `b` correspondant
s'annule **mod p** : `p | P(u^a)`. On évalue donc `P` aux `L` points `u^0 … u^(L-1)` (évaluation
multipoint sur arbre de sous-produits) et on prend `gcd` avec `n` -> `p`.

`u`, `v_b` s'obtiennent par multiplications successives (pas d'exponentiation par point).

## Implémentation (pas de Sage disponible)

Kali n'a ni Sage ni pari/flint ; `pip3 install --break-system-packages python-flint` fournit
FLINT, dont `fmpz_mod_poly_ctx` a **`multipoint_evaluate`** (l'API utile est `fmpz_mod_poly_ctx`,
pas `fmpz_mod_ctx`). Mesures :

| L | construction P | multipoint | total |
|---|---|---|---|
| 2^14 | 0.2 s | 0.7 s | 1 s |
| 2^17 | 13 s | 82 s | 95 s |
| **2^18** | 30 s | 205 s | **240 s** |

## PoW (md5, 24 bits)

8 processus (`mp.get_context("fork")` — **attention**, en Python 3.14 le contexte par défaut est
`forkserver`, les globals ne sont pas hérités : passer préfixe/cible **en argument**),
`imap_unordered` + `pool.terminate()` dès le premier succès (sinon on attend le plus lent).
~3-5 s.

## Déroulé réel

```
PoW prefixe=48757 cible=1177cb -> 4875711458567 (3.4 s)
n=1023 bits e=1023 bits
deg(P)=262144 construit en 29.9 s ; multipoint 205.4 s ; facteur trouve a a=73906
p+q envoye -> academy{p0lyn0m14l_...}
```

## Scripts

- [`solve.py`](../../solve/120/solve.py)
- [`_z_120_flag.txt`](../../solve/120/_z_120_flag.txt)
- [`_z_120url.txt`](../../solve/120/_z_120url.txt)
- *9 variantes intermediaires dans `solve/120/archive/`*
