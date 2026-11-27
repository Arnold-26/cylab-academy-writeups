# 417 — flag_printer

**Événement** : picoCTF 2024 · **Catégorie** : Cryptography · **Auteur** : non précisé dans les sources consultées

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Au secours ! J'ai encodé mon imprimante à flag avec un schéma d'encodage vraiment cool, et
maintenant je n'arrive plus à y accéder ! Pouvez-vous m'aider à retrouver le flag ? »

Le fichier fourni (`encoded.txt`) contient ~1 769 611 lignes de la forme `x y`, deux entiers
dans `GF(p)` avec `p = 7514777789`.

## Analyse

Ce ne sont pas des données brutes mais des **points d'échantillonnage d'un polynôme inconnu** :

```
f(x_i) = a_0 + a_1*x_i + ... + a_{n-1}*x_i^{n-1}  (mod p)
```

- `n` points distincts déterminent un unique polynôme de degré `n-1` → le retour se fait par
  **interpolation polynomiale de Lagrange**.
- Le degré est ≈ 1,77 million : c'est le vrai piège. L'algorithme de Lagrange naïf est
  quadratique (`~3·10^12` multiplications dans le corps) et ne termine jamais.
- Le corps premier `p` juste au-dessus de `2^32` garantit que chaque coefficient encode un
  octet sans ambiguïté — et le nom du challenge dit ce qu'on fait des octets : un **BMP**.
  Les deux premiers octets du résultat doivent être `42 4D` (`BM`).

## Solution

Interpolation **diviser pour régner** (subproduct tree / « Modern Computer Algebra » ch. 10) :
on coupe les points en deux, on calcule les polynômes d'annulation `Z1`, `Z2` de chaque
moitié, on ajuste `Y` par division par le `Z` de l'autre moitié, puis
`f = f1*Z2 + f2*Z1`. Complexité `O(n log² n)`.

Squelette SageMath (reproduit de la source publique `solve.sage`) :

```python
p = 7514777789
K = GF(p); R = PolynomialRing(K, 'x')
def compZ(X):
    x = R.gen(); Z = K(1)
    for xk in X: Z *= (x - xk)
    return Z
def comp(X, Y, Xother):
    Z = compZ(Xother); return [y / Z(x) for x, y in zip(X, Y)], Z
def solve(X, Y):
    if len(Y) <= 10: return R.lagrange_polynomial(list(zip(X, Y)))
    h = len(Y)//2
    Y1, Z2 = comp(X[:h], Y[:h], X[h:])
    Y2, Z1 = comp(X[h:], Y[h:], X[:h])
    return solve(X[:h], Y1) * Z2 + solve(X[h:], Y2) * Z1
f = solve(X, Y); coeffs = f.coefficients(sparse=False)
open('output.bmp','wb').write(bytearray(coeffs[:-1]))   # le dernier coefficient est en trop
```

Variante bien plus rapide : `python-flint` avec
`fmpz_mod_poly_ctx(fmpz_mod_ctx(7514777789)).interpolate(X, Y)` (~25 s).

Vérifications utiles : tester la récursion sur les 1000 premiers points avant de lancer le
calcul complet, et vérifier `0x42 0x4D` en tête du BMP. Un coefficient hors de `[0,256)`
signale une erreur de récursion (moitiés `Z1`/`Z2` inversées), pas un problème de données.

## Flag

Le flag est **dessiné** dans `output.bmp` ; la source publique qui a reconstruit l'image donne :

```
picoctf{i_do_hope_you_used_the_favorite_algorithm_of_every_engineering_student}
```

(forme publiée telle quelle, en minuscules ; à confirmer visuellement sur le BMP de votre
instance, le rendu image faisant foi.)

## Sources

- https://github.com/SuperBeetleGamer/Crypto-Writeups/blob/main/picoCTF%202024/Flag_printer/writeup.md
- https://picoctfsolutions.com/picoctf-2024-flag-printer
