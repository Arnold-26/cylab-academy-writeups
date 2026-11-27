# 417 — flag_printer

**Événement** : picoCTF 2024 · **Catégorie** : Cryptography

## Énoncé

L'énoncé raconte qu'une imprimante à flag a été encodée avec un schéma d'encodage « vraiment cool », et que son propriétaire n'arrive plus à y accéder : il faut retrouver le flag.

Le fichier fourni (`encoded.txt`) contient environ 1 769 611 lignes de la forme `x y`, deux entiers dans `GF(p)` avec `p = 7514777789`.

## Analyse

### Des points, pas des octets

Le fichier n'est pas une suite de données brutes mais des **points d'échantillonnage d'un polynôme inconnu** :

```
f(x_i) = a_0 + a_1*x_i + ... + a_{n-1}*x_i^{n-1}  (mod p)
```

- `n` points distincts déterminent un unique polynôme de degré `n-1` : le retour se fait par **interpolation polynomiale de Lagrange**.
- Le degré est d'environ 1,77 million : c'est le vrai piège. L'algorithme de Lagrange naïf est quadratique (environ `3*10^12` multiplications dans le corps) et ne termine jamais.
- Le corps premier `p` juste au-dessus de `2^32` garantit que chaque coefficient encode un octet sans ambiguïté.
- Le nom du challenge dit ce qu'on fait des octets : un **BMP**. Les deux premiers octets du résultat doivent être `42 4D`, soit `BM`.

### Pourquoi un BMP

Un BMP non compressé commence par un en-tête de 14 octets puis un en-tête DIB, et les pixels suivent en clair. Si les coefficients du polynôme sont les octets du fichier, alors les deux premiers forment la signature `BM` : c'est la vérification la plus simple pour savoir si l'interpolation est correcte, avant même de regarder l'image.

Le corps premier choisi est aussi une contrainte utile : chaque coefficient doit tomber dans `[0, 256)` pour être un octet. Un coefficient plus grand signale immédiatement une erreur d'algorithme, pas une bizarrerie des données.

## Solution

### Interpolation diviser pour régner

On utilise une structure de sous-produits (subproduct tree) : on coupe les points en deux, on calcule les polynômes d'annulation `Z1`, `Z2` de chaque moitié, on ajuste `Y` par division par le `Z` de l'autre moitié, puis `f = f1*Z2 + f2*Z1`. Complexité `O(n log² n)`.

Squelette SageMath :

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

### Variante flint

`python-flint` fait la même chose beaucoup plus vite :

```python
from flint import fmpz_mod_ctx, fmpz_mod_poly_ctx
ctx = fmpz_mod_poly_ctx(fmpz_mod_ctx(7514777789))
f = ctx.interpolate(X, Y)
```

Le calcul complet tombe autour de 25 secondes, contre plusieurs minutes pour la version Sage pure.

### Vérifications

Tester la récursion sur les 1000 premiers points avant de lancer le calcul complet, et vérifier `42 4D` en tête du BMP. Un coefficient hors de `[0, 256)` signale une erreur de récursion (moitiés `Z1`/`Z2` inversées), pas un problème de données.

### Pourquoi ça marche

Chaque ligne est une évaluation du polynôme en un point. Avec `n` points distincts, l'interpolation redonne les coefficients de façon unique : c'est le théorème d'interpolation. Le corps premier permet une arithmétique exacte, sans erreur d'arrondi, et les coefficients se relisent directement comme des octets puisque le polynôme a été construit à partir d'eux.

## Pièges

- **Lagrange naïf** : `O(n²)` avec `n` proche de 1,77 million, le calcul ne finit jamais.
- **Moitiés inversées** : `Z1` et `Z2` échangés donnent un polynôme faux, avec des coefficients hors bornes.
- **Coefficient final** : le polynôme à un coefficient de plus que le nombre d'octets ; `coeffs[:-1]` le retire.
- **Tester en base entière** : sans réduction modulo `p`, les divisions n'ont pas de sens dans le corps.
- **Oublier d'ouvrir le BMP** : le flag est dessiné dans l'image, pas lisible dans les octets bruts.
- **Mémoire** : la structure de sous-produits tient en mémoire pour 1,7 million de points, mais seulement si on évite les copies inutiles.
