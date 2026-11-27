# Guess My Cheese (Part 1)

**Catégorie** : Cryptography · **Challenge** : #473 · **Résolu le** : 2026-11-24

## Énoncé

> nc chatelaine.cylabacademy.net <port>

## Résolution

Méthode : **chiffrement affine + oracle d'encryption (CHEDDAR) -> 312 cles**.

Le service affiche un fromage secret chiffre et propose deux commandes : `g` (deviner) et `e` (chiffrer). C'est un **chiffrement affine** E(x) = (a*x + b) mod 26 sur A-Z, avec une cle **aleatoire par session** et seulement 3 tentatives. Le piege : l'oracle n'accepte que de VRAIS noms de fromages (envoyer `aaaaaaaaaa` consomme une tentative pour rien) et il ignore silencieusement tout caractere hors A-Z. Il faut donc envoyer un fromage connu, par exemple **CHEDDAR**, ce qui donne une paire clair/chiffre ; deux lettres suffisent pour resoudre le systeme (2a+b et 7a+b modulo 26). On peut aussi brute-forcer les 312 cles (12 valeurs de a inversibles x 26 valeurs de b) : c'est instantane et sans risque d'erreur de calcul. Avec (a,b) on dechiffre le fromage secret par D(y) = a^-1 * (y - b) mod 26, puis on l'envoie via `g`. Les noms sont volontairement exotiques (« they might look different from cheeses you're used to ») : ici le secret etait `TOMAI`, et la soumission a fonctionne en majuscules.

## Flag

```
academy{ChEeSy8b0897b1}
```

## Scripts

- [`solve.py`](../../solve/473/solve.py)
- *7 variantes intermediaires dans `solve/473/archive/`*
