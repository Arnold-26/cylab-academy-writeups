# la cifra de

**Catégorie** : Cryptography · **Challenge** : #3 · **Résolu le** : 2026-11-23

## Énoncé

> I found this cipher in an old book.

## Résolution

Méthode : **vigenere avec clé derivee du clair connu**.

Le message est chiffré en Vigenere. On connait un fragment de clair probable : `Brftsk ip Volpnexj` = `Blaise de Vigenere`. En calculant (chiffre - clair) mod 26 on obtient la sequence `a,g,f,l,a,g,f,l...` -> la clé est **`flag`** avec un décalage de 3 dans le message. Déchiffre, le texte parle de Bellaso et du chiffre de Vigenere, et le flag est à la fin.

## Flag

```
academy{b311a50_0r_v1gn3r3_c1ph3r36311a0a}
```
