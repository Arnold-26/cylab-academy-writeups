# triple-secure

**Catégorie** : Cryptography · **Challenge** : #209 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **gcd des modules partages**.

Trois modules RSA partagent leurs facteurs deux a deux : `n1 = pq`, `n2 = pr`, `n3 = qr`. Un simple `gcd(n1, n2)` donne p, etc. On inverse ensuite les trois chiffrements successifs (dans l'ordre inverse) avec les phi correspondants.

## Flag

```
picoCTF{1_gu3ss_tr1pl3_rs4_1snt_tr1pl3_s3cur3!!!!!!}
```

## Ce qu'il faut retenir

—
