# 107 — Scrambled: RSA — Cryptography

**Flag :** `academy{bad_1d3a5_73efa9c}`
**Cible :** `nc chatelaine.cylabacademy.net <port>`

## Le service

```
flag: <~8300 chiffres>
n: <308 chiffres>          (1024 bits)
e: 65537
I will encrypt whatever you give me:
```
puis, pour chaque ligne envoyée : `Here you go: <nombre>`

## Mesures (l'essentiel du travail)

| requête | longueur du chiffré |
|---|---|
| `a` | 308 |
| `aa` | 616 |
| `aaa` | 924 |
| `ab` | 617 |
| `ba` | 616 |
| `1` | 307 |

Relations exactes mesurées :
- `enc("a")` est un **préfixe** de `enc("aa")` et de `enc("ab")` ;
- `enc("a")` **n'est pas** une sous-chaîne de `enc("ba")` ;
- `enc("b")` est un **suffixe** de `enc("ba")` mais **absent** de `enc("ab")` ;
- `enc("aa")` est un **suffixe** de `enc("aaa")` alors que `enc("aaa")` ne commence pas par `enc("aa")`.

Conclusion : le chiffré est la **concaténation, dans un ordre mélangé**, d'un bloc RSA par
caractère. Chaque bloc fait 306-309 chiffres (valeur RSA aléatoire, **non padée**), et le bloc
dépend de **la position ET du caractère** (sinon `enc("a")` serait dans `enc("ba")`).
`pow(ord(c), 65537, n)` ne correspond à aucun bloc -> chaque bloc est un RSA « salé »
(dépendant de la position) ; c'est pour ça que la table de caractères construite naïvement ne
donnait rien.

## L'attaque (validée)

Pour une position `k`, le bloc `B_k(c)` est déterministe. Donc :
1. `enc(prefixe)` = concaténation mélangée de `B_1..B_k` ;
2. en retirant les blocs déjà connus, il reste exactement `B_k` ;
3. `B_k` doit être une **sous-chaîne** du chiffré du flag (puisque le flag contient le bloc de
   la même position).

Boucle, caractère par caractère :

```python
enc = query(prefix + c)          # oracle
for k in known: enc = enc.replace(k, '')
if enc in flag_work:             # bloc de la nouvelle position
    flag_work = flag_work.replace(enc, '', 1)
    known.append(enc); prefix += c
```

Le préfixe `academy{` est connu : on peut l'amorcer en 1 requête par position (gain de ~200
requêtes), puis chercher la suite. Charset : `a-z0-9_{}` puis majuscules/ponctuation.

Résultat (207 requêtes, 82 s) :

```
academy{bad_1d3a5_73efa9c}
```

## Scripts

- [`_z_107_banner.txt`](../../solve/107/_z_107_banner.txt)
- [`_z_107_brute.py`](../../solve/107/_z_107_brute.py)
- [`_z_107_data1.json`](../../solve/107/_z_107_data1.json)
- [`_z_107_data1.txt`](../../solve/107/_z_107_data1.txt)
- [`_z_107_data2.json`](../../solve/107/_z_107_data2.json)
- [`_z_107_data4.json`](../../solve/107/_z_107_data4.json)
- [`_z_107_dec.py`](../../solve/107/_z_107_dec.py)
- [`_z_107_diag.py`](../../solve/107/_z_107_diag.py)
- [`_z_107_fixed.py`](../../solve/107/_z_107_fixed.py)
- [`_z_107_flag.txt`](../../solve/107/_z_107_flag.txt)
- [`_z_107_join.py`](../../solve/107/_z_107_join.py)
- [`_z_107_join2.py`](../../solve/107/_z_107_join2.py)
- [`_z_107_join3.py`](../../solve/107/_z_107_join3.py)
- [`_z_107_join4.py`](../../solve/107/_z_107_join4.py)
- [`_z_107_limit.py`](../../solve/107/_z_107_limit.py)
- [`_z_107_map.py`](../../solve/107/_z_107_map.py)
- [`_z_107_oracle.py`](../../solve/107/_z_107_oracle.py)
- [`_z_107_pad.py`](../../solve/107/_z_107_pad.py)
- [`_z_107_probe.py`](../../solve/107/_z_107_probe.py)
- [`_z_107_probe1.py`](../../solve/107/_z_107_probe1.py)
