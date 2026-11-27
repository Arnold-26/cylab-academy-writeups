# 709 — MSS_ADVANCE Revenge

**Événement** : picoCTF 2026 · **Catégorie** : Cryptography

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
Un schéma de partage de secret « modified Shamir » qui se trahit par sous-détermination : les
fichiers `chall.py` et `output.txt` sont fournis, et `MASTER_KEY` chiffre le flag en AES-CBC.

## Analyse
`chall.py` construit un polynôme de degré 29 sur un corps premier `p` de 1024 bits, avec 30
coefficients `c_0 … c_29`. Chaque coefficient est dérivé du précédent par `c_(i+1) = SHA-256(c_i)`,
donc tous valent environ 256 bits. Le coefficient de tête `c_0` **est** `MASTER_KEY`, soit
`sha256(flag)` interprété comme entier.

Problème : seuls 20 points `(x_i, f(x_i))` sont publiés, pour 30 inconnues. Le système linéaire
modulo `p` est donc sous-déterminé et l'algèbre linéaire classique ne suffit pas. L'astuce est que
le vecteur solution est **anormalement court** par rapport à `p` (256 bits contre 1024) : c'est
exactement le profil d'une attaque par réduction de réseau (LLL).

## Solution
1. Construire une matrice entière `(m+n+1) × (m+n+1)` avec `m = 20` équations et `n = 30`
   inconnues, en absorbant l'arithmétique modulaire par `p·W` sur la diagonale (poids `W = 2^512`),
   les puissances `x_i^(n-1-j) mod p` dans les lignes d'équations, et `-f(x_i)·W` dans la dernière
   ligne.
2. Réduire avec LLL (SageMath).
3. Dans la matrice réduite, toute entrée entre 250 et 260 bits est candidate pour `MASTER_KEY` :
   la convertir en 32 octets big-endian et l'utiliser comme clé AES-CBC (IV de 16 octets à zéro,
   codé en dur), puis chercher `picoCTF` dans le clair déchiffré.

```bash
cat chall.py
cat output.txt
grep -nE 'def |%|pow|coeff|MASTER|share|range' chall.py   # confirme 30 coefficients, 20 évaluations
# matrice + LLL en SageMath, puis déchiffrement AES-CBC (script du writeup)
```
Piège classique : `MASTER_KEY` est déjà un digest SHA-256 ; le re-hacher donne une mauvaise clé.

## Flag
```
flag non conservé
```
La page de solution publique ne publie pas la valeur du flag pour ce challenge ; seul le chemin
d'attaque (LLL puis AES-CBC) est documenté.

## Sources
- https://picoctfsolutions.com/picoctf-2026-mss-advance-revenge — page de solution picoCTF 2026 (structure du polynôme, construction du réseau, extraction de `MASTER_KEY`)
