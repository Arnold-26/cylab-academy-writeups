# Clouds

**Catégorie** : Cryptography · **Challenge** : #136 · **Événement** : picoCTF 2021

## Énoncé

> Cloud watching is a lot of fun! There are so many different shapes you see in them, and so many different types. They even inspired me to dig up an old cipher I once found to store notes about them. See if you can decrypt them!

## Flag

```
0b48d5adb3074b90
```

(le challenge précise : **pas** d'enveloppe `academy{}`)

## Le chiffre : Nimbus (Furman)

`clouds.py` (Python 2.7) chiffre des blocs de 8 octets, clé de 40 octets = 5 sous-clés,
5 tours. Un tour :

```
y = g(x XOR k_i) * (k_i | 1)  mod 2^64        g = inversion des 64 bits
```

`notes[0] = encrypt(flag)` est le texte chiffré du flag ; on peut stocker jusqu'à 2048 notes
de 512 octets et relire n'importe quelle note → un oracle d'chiffrement massif
(2048 × 64 = 131 072 blocs disponibles).

## L'attaque : cryptanalyse différentielle

Différentiel de Furman `Δ = 2^63 − 2 = 0x7FFF…FE` (palindromique, donc `g(Δ) = Δ`).

**Lemma 1** : pour `A`, `B` pairs, `A XOR B = Δ  ⟺  A + B = Δ`.

**Récupérer `o_i = k_i | 1`** : soit une paire avec `x XOR x' = Δ` (les valeurs `A = g(x XOR k_i)`,
`A' = g(x' XOR k_i)` vérifient alors `A XOR A' = Δ`). Si `A` est pair, Lemma 1 donne
`A + A' = Δ`, donc

```
y + y' = Δ * o_i      =>      o_i mod 2^63 = ((y+y')/2) * (Δ/2)^(-1)  mod 2^63
```

`Δ/2 = 2^62 − 1` est **impair**, donc inversible mod `2^63` (l'octet de poids fort de `o_i`
reste inconnu ; son bit 0 vaut 1 puisque `o_i` est impair). Le **mode** de cette valeur sur des
milliers de paires est `o_i` : la différence survit à chaque tour avec probabilité 1/2, donc la
fraction de paires encore « utiles » au tour `i` est `2^-(i-1)`.

**Deux pièges mesurés (c'était le cœur du travail)** :

1. **Les paires à multiplicande impair polluent le mode.** Si `A` est impair, on a
   exactement `A + A' = Δ + 2 = 2^63`, donc `y + y' ≡ 2^63` et **toutes** ces paires votent
   pour la constante `2^62`. Elles peuvent battre la vraie valeur (observées 509 contre 499).
   Comme `o_i` est impair, `o_i ≠ 2^62` : il suffit de **jeter le vote `2^62`**.
2. **Le tour 1 est dégénéré.** La différence d'entrée y vaut `Δ` par construction et, par
   Lemma 1, `P + P' = Δ` : l'équation de somme donne `o_1 · Δ = Δ`, c'est-à-dire `o_1 ≡ 1`.
   La récupération de `k_1` se fait donc **autrement** : avec deux clairs `P` et `P XOR 2^63`,
   on a `u' = u XOR 1` (car `g(2^63) = 1`), donc
   `y' − y = ±o_1` **exactement** → `o_1 = ±d` (deux candidats), puis
   `k_1 = g(y · o_1^(-1)) XOR P` avec la vérification `k_1 | 1 == o_1`.

**Vérification finale** : les blocs 0..2 (`0`, `Δ`, `2^63`) sont trop structurés — plusieurs
variantes de clé y donnent le même chiffré. Vérifier sur ~7 blocs génériques répartis, puis
garder le texte clair le plus imprimable.

## Données et coût

8192 blocs = **4096 paires Δ** (128 notes de 512 o, chacune contenant 16 groupes
`A, A^Δ, A^2^63, (A^2^63)^Δ`), soit ~5 s de calcul. On peut descendre à 1024 paires
(2048 blocs) sans échec sur 8 graines testées.

## Reproduire

```bash
python3 _z_136_solve.py selftest 2048                  # 8 graines OK
python3 _z_136_solve.py <host> <port> 2048             # instance réelle (~2 min)
```

Script : `_z_136_solve.py` (contient aussi un serveur local `--server` pour tester
le protocole de bout en bout, et `local` pour le test complet).

## Scripts

- [`solve.py`](../../solve/136/solve.py)
- *9 variantes intermediaires dans `solve/136/archive/`*
