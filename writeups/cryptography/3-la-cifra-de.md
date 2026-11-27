# la cifra de

**Catégorie** : Cryptography · **Challenge** : #3 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **vigenere avec cle derivee du clair connu**.

Le message est chiffre en Vigenere. On connait un fragment de clair probable : `Brftsk ip Volpnexj` = `Blaise de Vigenere`. En calculant (chiffre - clair) mod 26 on obtient la sequence `a,g,f,l,a,g,f,l...` -> la cle est **`flag`** avec un decalage de 3 dans le message. Dechiffre, le texte parle de Bellaso et du chiffre de Vigenere, et le flag est a la fin.

## Flag

```
academy{b311a50_0r_v1gn3r3_c1ph3r36311a0a}
```

## Ce qu'il faut retenir

—
