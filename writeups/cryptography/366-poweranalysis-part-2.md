# PowerAnalysis: Part 2

**Catégorie** : Cryptography · **Challenge** : #366 · **Résolu le** : 2026-11-25

## Énoncé

> The encryption leaks one bit per computation.

## Résolution

Méthode : **leak oracle**.

Ici pas de traces : `encrypt.py` (fourni) fait

```python
leak_buf.append(Sbox[plaintext[i] ^ key[i]] & 0x01)
...
return leak_buf.count(1)
```

Le serveur renvoie donc **la somme des LSB** des 16 sorties de S-box, soit un entier de 0 a 16.

### Attaque adaptative, ~9 requetes par octet

Baseline : plaintext tout a zero -> `t0 = 8`.

Ensuite, pour l'octet `i`, on ne fait varier que lui (les 15 autres restent a 0) avec une
valeur `v`, et on regarde `delta = t - t0` :

| delta | contrainte |
|---|---|
| +1 | `Sbox[v^k]&1 = 1` **et** `Sbox[k]&1 = 0` |
| -1 | `Sbox[v^k]&1 = 0` **et** `Sbox[k]&1 = 1` |
| 0 | `Sbox[v^k]&1 = Sbox[k]&1` |

Chaque requete coupe l'ensemble des 256 candidats en deux : 8 a 11 requetes suffisent pour
isoler l'octet. Cout total : **~140 connexions**, quelques minutes.

Une seule requete par connexion (le script fait `input()` une fois), et la clef est stable
entre les connexions.

```
KEY: 290fda44a3d9bd690a8dba3e760f5a7e
```

### A retenir

- Un oracle qui renvoie **une somme sur 16 octets** n'est pas aveugle : en ne bougeant qu'un
  octet a la fois, la variation `-1/0/+1` donne un bit sur cet octet.
- Toujours garder la contrainte *complete* (`f(v,k)` ET `f(0,k)`), sinon on garde des faux
  candidats : c'est ce qui fait la difference entre 9 requetes et 256.

## Flag

```
academy{290fda44a3d9bd690a8dba3e760f5a7e}
```
